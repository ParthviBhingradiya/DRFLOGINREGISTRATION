from django.shortcuts import render
from .models import Student
from .serializers import StudentSerializer
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# Create your views here.

# class StudentRegister(viewsets.ModelViewSet):
#     queryset=Student.objects.all()
#     serialize_classes=StudentSerializer
#     # authentication_classes=[JWTAuthentication]
#     # permission_classes=[IsAuthenticated]


class StudentRegister(viewsets.ModelViewSet):
    queryset=Student.objects.all()
    serializer_class=StudentSerializer

class StudentLogin(viewsets.ModelViewSet):
    """
    An endpoint to authenticate existing users using their email and password.
    """
    def post(self,request,formate=None):
        return Response({'msg':'Login Success'})