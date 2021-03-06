from attr import fields
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm 
from . models import QuizQuestion

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class EditProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['username' ,'email']


class AddQuestionForm(ModelForm):
    class Meta:
        model = QuizQuestion
        fields = ['question_title' , 'option1' , 'option2', 'option3', 'option4', 'answer']


class EditQuestions(ModelForm):
    class Meta:
        model = QuizQuestion
        fields =   ['question_title' , 'option1' , 'option2', 'option3', 'option4', 'answer']
