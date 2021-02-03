from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('question/<int:quiz_id>/<int:qno>', question, name="question"),
    path('answer/<int:quiz_id>', answer, name='answer'),
    path('result/<int:quiz_id>', result, name='result'),
    path('register/', register, name='register'),
    path('login/', slogin, name='login'),
    path('logout/', slogout, name='logout')
]
