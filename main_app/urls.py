from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('quiz/<int:quiz_id>/', views.quiz, name='quiz'),
    path('submit_answer/', views.submit_answer, name='submit_answer'),
    path('result/<int:quiz_id>/', views.result, name='result'),
]
