from django.urls import path 
from . import views

urlpatterns = [

    path('',views.quiz_question, name='Home'),
    
    path('register/' , views.register , name = 'register'),
    path('login/',views.Login, name='login'),
    path('logout/',views.Logout ,name = "logout" ),

    path('edit-profile',views.UpdateProfile , name= "edit-profile"),
    path('user-profile/<str:pk>',views.UserProfile , name= "user-profile"),

    path('add-question/',views.CreateQuestion , name= "add-question"),
    path('delete-question/<str:pk>',views.Delete_Question , name= "delete-question"),
    path('edit-question/<str:pk>',views.Edit_Question , name= "edit-question"),

    path('check-question/<str:pk>',views.Check_Question , name= "check-question"),

    path('forgot-password/',views.Forgot_Password , name= "forgot-password"),
    
] 