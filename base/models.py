from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class QuizQuestion(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    question_title = models.TextField(null=True)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200) 
    answer = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.question_title 
    
    class Meta:
        ordering = ['-created']