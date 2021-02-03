from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Student)
admin.site.register(StudentAnswer)
admin.site.register(QuizResults)
