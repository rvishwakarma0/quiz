from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


CHOICE_ID = [
    ('a', 'a'),
    ('b', 'b'),
    ('c', 'c'),
    ('d', 'd'),
]


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=2000)
    answer = models.CharField(max_length=1, choices=CHOICE_ID)
    a = models.CharField(max_length=500)
    b = models.CharField(max_length=500)
    c = models.CharField(max_length=500)
    d = models.CharField(max_length=500)

    def __str__(self):
        return self.question_text


class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1, choices=CHOICE_ID)

    def __str__(self):
        return self.answer

class QuizResults(models.Model):
    start_time = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    score = models.IntegerField(default= 0, blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.student.user.username