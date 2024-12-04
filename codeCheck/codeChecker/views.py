from django.shortcuts import render, redirect
from .models import Submission, Lesson, Student
from .forms import SubmissionForm, LessonSelectForm
import difflib


def submit_code(request):
    form = SubmissionForm(request.POST or None)
    comparison_results = None  # Инициализируем переменную для результатов сравнения

    if request.method == 'POST' and form.is_valid():
        student = form.cleaned_data['student']
        lesson = form.cleaned_data['lesson']
        code = form.cleaned_data['code']

        # Обновляем или создаем новую запись
        submission, created = Submission.objects.update_or_create(
            student=student, lesson=lesson,
            defaults={'code': code}
        )

        # Подготовка данных для сравнения кодов
        submissions = Submission.objects.filter(lesson=lesson).exclude(id=submission.id)
        comparison_results = []
        for other_submission in submissions:
            similarity = difflib.SequenceMatcher(None, submission.code, other_submission.code).ratio() * 100
            formatted_similarity = f"{similarity:.2f}"  # Форматируем до 2 знаков после запятой используя f-строку
            comparison_results.append((other_submission.student.full_name, formatted_similarity))

        # Можно также обновить страницу, чтобы показать результаты
        # Но здесь мы покажем результаты сразу на этой же странице

    return render(request, 'codeChecker/submit_code.html', {
        'form': form,
        'comparison_results': comparison_results
    })


def results(request):
    lesson_id = request.GET.get('lesson')
    form = LessonSelectForm(request.GET or None)
    students = Student.objects.all().order_by('full_name')
    submissions = Submission.objects.filter(lesson_id=lesson_id).select_related('student', 'lesson') if lesson_id else Submission.objects.none()
    results_matrix = {student.full_name: {other.full_name: '-' for other in students} for student in students}

    if submissions:
        for sub1 in submissions:
            for sub2 in submissions:
                if sub1 != sub2:
                    similarity = difflib.SequenceMatcher(None, sub1.code, sub2.code).ratio() * 100
                    results_matrix[sub1.student.full_name][sub2.student.full_name] = f"{similarity:.2f}%"

    return render(request, 'codeChecker/results.html', {
        'form': form,
        'results_matrix': results_matrix,
        'students': students,
        'submissions': submissions if lesson_id else None  # Добавляем submissions в контекст
    })
