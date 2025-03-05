from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Student
from django.contrib.auth import authenticate




class StudentSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Student  
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2') 
        return Student.objects.create_user(**validated_data) 

class StudentLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields=['username','password']

