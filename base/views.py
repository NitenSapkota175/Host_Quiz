from distutils.command.install_data import install_data
from turtle import right
from django.shortcuts import render,redirect
from pendulum import instance
from . models import QuizQuestion
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from . forms import EditProfileForm, UserForm,EditQuestions
from django.contrib import messages

# Create your views here.

def  quiz_question(request):
    

     questions = QuizQuestion.objects.all()[0:20]
     context  = { 'questions' : questions}
     if request.method == 'POST':
         answer = request.POST.get('answer')
         title = request.POST.get('q')
         question = QuizQuestion.objects.get(question_title=title)
         answer1 = questions.answer
         if answer== answer1:
             isanswer = 'Right'
             context = {'isanswer' : isanswer , 'questions' : questions}
             
             return render(request,'base/Home.html',context)
         else:
             isanswer = 'Wrong'
             context = {'isanswer' : isanswer , 'questions' : questions}
             return render(request,'base/Home.html',context)

     return render(request,'base/Home.html' ,context ) 

def register(request):
    form = UserForm()
    if request.method == 'POST':
       form =  UserForm(request.POST)
       if form.is_valid():
           user = form.save(commit=False)
           user.username = user.username.lower()
           user.save()
           login(request,user)
           return redirect('Home')
       else:
           messages.error(request,"An error occurred during registartions")

       

    return render(request,'base/login_register.html',{'form' : form})

def Login(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
          user = User.objects.get(username=username)
        except:
            messages.error(request,"User desnot exists")
        user = authenticate(request,username = username, password=password)
        if user is not None:
            login(request,user)
            return redirect('Home')
        else:
            messages.error(request,"User credentails is invalid")
    return render(request,'base/login_register.html',{'page' : page})

def Logout(request):
    logout(request)
    return redirect('Home')

def UpdateProfile(request):
    user = request.user
    form = EditProfileForm(instance=user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST,instance=user)
        if form.is_valid():
          form.save()
          return redirect('Home')
        else:
            messages.error(request,'Error occurred' )    
        
    return render(request,'base/EditProfile.html',{'form' : form})


def UserProfile(request,pk):
    
    user = User.objects.get(id=pk)
    question =  user.quizquestion_set.all()
    context = {'question' : question}
    return render(request,'base/user_profile.html',context)

def Edit_Question(request,pk):
    question = QuizQuestion.objects.get(id=pk)
    form = EditQuestions(instance=question)
    if request.user == question.user:
            if request.method == 'POST':
                form = EditQuestions(request.POST,instance=question)
                if form.is_valid():
                    form .save()
                    return redirect('Home')

                else:
                    messages(request,'Some errror occurred')
    else:  
        messages.error(request,'Message you are not allowed edit this question cause you are not the host  ')
        return redirect('Home')

    return render(request,'base/edit-question.html',{'form' : form})

def Delete_Question(request,pk):

    question = QuizQuestion.objects.get(id=pk)
    if question.user == request.user:
        question.delete()
        return redirect ('Home')
    else:
        messages.error(request,"Your are not allowed ")
    