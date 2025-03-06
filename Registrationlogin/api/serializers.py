# from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from .models import User  

class StudentSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User 
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

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
    password=serializers.CharField(max_length=8)

    class Meta:
        model=User
        fields=['username','password']

# class StudentLoginSerializer(serializers.Serializer): 
#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True, style={'input_type': 'password'})

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','first_name','last_name','email']

class ChangeSerializer(serializers.Serializer):
    password=serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2=serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        fields=['password','password2']

    # def validate(self, attrs):
    #     password=attrs.get('password')
    #     password2=attrs.get('password2')
    #     if password
    #     return attrs)

