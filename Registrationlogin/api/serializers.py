# from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from .models import User , ApplicationForm
import re

class StudentSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    role=serializers.ChoiceField(choices=[('student','Student'),('teacher','Teacher')],required=True)


    class Meta:
        model = User 
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password', 'password2','role']
        extra_kwargs = {'password': {'write_only': True}}


    def validate_password(self, value):
     
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character (!@#$%^&* etc.).")
        return value
    
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2') 
        print('validated_data: ', validated_data)
        return User.objects.create_user(**validated_data) 
    
    
class StudentLoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField(min_length=8)

    class Meta:
        model=User
        fields=['username','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','first_name','last_name','email']


class StudentApplicationSerializer(serializers.ModelSerializer):
    study_mode = serializers.ChoiceField(choices=[('online', 'Online'), ('offline', 'Offline')], required=True)

    class Meta:
        model = ApplicationForm
        fields = ['id', 'user', 'university_name', 'program_name', 'description', 'study_mode', 'from_date', 'to_date']

    def validate(self, data):
        from_date = data.get('from_date')
        to_date = data.get('to_date')

        if from_date and to_date and to_date <= from_date:
            raise serializers.ValidationError({"to_date": "to_date must be greater than from_date."})

        return data

           

class StudentLeaveListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ApplicationForm
        fields = ['university_name', 'program_name', 'description', 'study_mode','from_date', 'to_date','status']


class TeacherShowStudentList(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)  
    last_name = serializers.CharField(source='user.last_name', read_only=True)  

    class Meta:
        model=ApplicationForm
        fields=['id','first_name','last_name','university_name', 'program_name', 'description', 'study_mode','from_date', 'to_date']


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationForm
        fields = ['status']  
