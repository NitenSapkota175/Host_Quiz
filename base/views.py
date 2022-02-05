from distutils.command.install_data import install_data
from turtle import right
from django.shortcuts import render,redirect
from matplotlib.style import context
from pendulum import instance
from rx import create
from . models import QuizQuestion
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from . forms import EditProfileForm, UserForm,EditQuestions,AddQuestionForm
from django.contrib import messages
from django.db.models import Q

# Create your views here.

def  quiz_question(request):
    q = request.POST.get('q') if request.POST.get('q') != None else  ''   
    
    

    questions = QuizQuestion.objects.filter(Q(question_title__icontains=q))[0:20]
    context  = { 'questions' : questions}
    

    return render(request,'base/Home.html' ,context ) 

@login_required(login_url='login')
def CreateQuestion(request):
   
    form = AddQuestionForm()
    if request.method == 'POST':
        
        question = QuizQuestion.objects.filter(question_title=request.POST.get('question_title'))

        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        answer = request.POST.get('answer')
        if option1 == option2 or option1 == option3 or option1 == option4 or option2==option3 or option2==option4 or option3==option4:
            messages.error(request,"Options should be different")
            return redirect('add-question')
        if option1!=answer and option2!=answer and option3!=answer and option4!=answer:
               messages.error(request,"One of the options should match with answer")
               return redirect('add-question') 

        if question.exists():
            
                messages.error(request,'Question already exists')
                return redirect('add-question')
        else:   
            QuizQuestion.objects.create(
                    user= request.user,
                    question_title = request.POST.get('question_title'),
                    option1 = option1,
                    option2 = option2,
                    option3 = option3,
                    option4 = option4,
                    answer = answer,
                )
            return redirect('Home')
    context = {'form' : form}
    return render(request,'base/add_question.html',context)





@login_required(login_url='login')
def Check_Question(request,pk):
    show = 0
    question = QuizQuestion.objects.get(id=pk)
    context = {'q' : question,'show' : show}
    if request.method == 'POST':
         show=1
         answer = request.POST.get('answer')
         
        
         answer1 = question.answer
         if answer== answer1:
             isanswer = 1
             context = {'isanswer' : isanswer ,'q' : question ,'show' : show}
             return render(request,'base/check-question.html',context)
         else:
             isanswer = 0
             context = {'isanswer' : isanswer ,'q' : question, 'show' : show}
             return render(request,'base/check-question.html',context )
    
    return render(request,'base/check-question.html',context)


@login_required(login_url='login')
def Edit_Question(request,pk):
    question = QuizQuestion.objects.get(id=pk)
    form = EditQuestions(instance=question)
    if request.user == question.user:
      if request.method == 'POST':
            option1 = request.POST.get('option1')
            option2 = request.POST.get('option2')
            option3 = request.POST.get('option3')
            option4 = request.POST.get('option4')
            answer = request.POST.get('answer')
            if option1 == option2 or option1 == option3 or option1 == option4 or option2==option3 or option2==option4 or option3==option4:
                    messages.error(request,"Options should be different")
                    return redirect('add-question')
            if option1!=answer and option2!=answer and option3!=answer and option4!=answer:
                    messages.error(request,"One of the options should match with answer")
                    return redirect('add-question') 
               
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



@login_required(login_url='login')
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


@login_required(login_url='login')
def Forgot_Password(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        if user is not None:
            user.set_password(request.POST.get('password'))
            user.save()
            return redirect('Home')
        
    return render(request,'base/forgot_password.html')


@login_required(login_url='login')
def UserProfile(request,pk):
    
    user = User.objects.get(id=pk)
    question =  user.quizquestion_set.all()
    context = {'question' : question}
    return render(request,'base/user_profile.html',context)





@login_required(login_url='login')
def Delete_Question(request,pk):

    question = QuizQuestion.objects.get(id=pk)
    if question.user == request.user:
        question.delete()
        return redirect ('Home')
    else:
        messages.error(request,"Your are not allowed ")
    