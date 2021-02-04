from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
import datetime


def dashboard(request):
    quizzes = Quiz.objects.all()
    context = {'quizzes': quizzes}
    return render(request, 'quiz/dashboard.html', context)


def question(request, quiz_id, qno):
    student = request.user.student
    user = request.user
    student = Student.objects.get(user = user)
    quiz = Quiz.objects.get(id=quiz_id)
    quiz_result, created = QuizResults.objects.get_or_create(quiz=quiz, student=student)
    if quiz_result.end_time :
        return redirect('/result/'+str(quiz_id))
    try:
        if qno == 0 :
            ques = quiz.question_set.all()[0]
            quiz_result.score = 0
            quiz_result.save()
        else:
            ques = quiz.question_set.all()[qno]

    except IndexError:
        # this means questions are over now
        quiz_result.end_time = datetime.datetime.now()
        quiz_result.save()
        return redirect('/result/'+str(quiz_id))
    qno += 1
    context = {'question': ques, 'quiz_id': quiz_id, 'qno':qno}
    return render(request, 'quiz/question.html', context)


def answer(request, quiz_id):
    msg = ""
    if request.method == 'POST':
        student = request.user.student

        qid = request.POST['qid']
        choice = request.POST['choice']

        quiz = Quiz.objects.get(id = quiz_id)
        ques = Question.objects.get(id=qid)
        quiz_result = QuizResults.objects.get(student=student, quiz=quiz)
        try:
            student_answer = StudentAnswer.objects.get(question=ques, answer=choice, student=student)
            return HttpResponse('already attempted')
        except:
            student_answer = StudentAnswer.objects.create(question=ques, answer=choice, student=student)
            student_answer.save()
        if ques.answer == choice:
            msg = "correct answer!"
            quiz_result.score += 1
            quiz_result.save()
        else:
            msg = "incorrect answer ! right answer is " + ques.answer
    return HttpResponse(msg)


def result(request, quiz_id):
    student = request.user.student
    quiz = Quiz.objects.get(id = quiz_id)
    quiz_result = QuizResults.objects.get(student=student, quiz=quiz)
    student_answer = StudentAnswer.objects.all()
    context = {
        'start_time' : str(quiz_result.start_time),
        'end_time' : str(quiz_result.end_time),
        'score' : quiz_result.score,
        'quiz' : quiz,
        'student_answer' : student_answer
    }
    return render(request, 'quiz/result.html', context)


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user, created = User.objects.get_or_create(username = username)
        print(password)
        user.set_password(password)
        user.save()
        student, created = Student.objects.get_or_create(user=user)
        student.save()
        return redirect('/login/')
    return render(request,'quiz/register.html')


def slogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request,user)
            return redirect('/')
    return render(request,'quiz/login.html')


def slogout(request):
    logout(request)
    return HttpResponseRedirect('/')