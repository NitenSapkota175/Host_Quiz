from django.shortcuts import render
from . models import QuizQuestion
from django.contrib.auth.models import User  
# Create your views here.

def  quiz_question(request):
    

     questions = QuizQuestion.object.all()[0:50]
     context  = {}
     return render(request,'base/Home.html' , context ) 