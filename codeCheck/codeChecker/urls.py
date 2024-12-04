from django.urls import path
from . import views

urlpatterns = [
    path('', views.submit_code, name='submit_code'),
    path('results/', views.results, name='result_page'),
]