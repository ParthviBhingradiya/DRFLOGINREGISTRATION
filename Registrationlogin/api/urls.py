from django.urls import path
from api import views

urlpatterns = [
    path('register/',views.StudentRegister.as_view(),name='register'),
    path('Login/',views.StudentLogin.as_view(),name='login'),
    path('profile/',views.UserProfileView.as_view(),name='profile'),


]
