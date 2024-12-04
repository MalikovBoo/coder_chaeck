from django.db import models


class Lesson(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Student(models.Model):
    full_name = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


class Submission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    code = models.TextField()
    submission_time = models.DateTimeField(auto_now_add=True)
