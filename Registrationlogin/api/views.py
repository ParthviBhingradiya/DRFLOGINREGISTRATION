from .serializers import StudentSerializer,StudentLoginSerializer,UserProfileSerializer,ChangeSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class StudentRegister(APIView):
    def post(self, request, format=None):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Registration Success.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentLogin(APIView):        
    def post(self, request, format=None):
        serializer = StudentLoginSerializer(data=request.data)
        print('serializer: ', serializer)
        
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': 'Login Success.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
            
class UserProfileView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,formate=None):
        serializer=UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class UserChangePasswordView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,formate=None):
        serializer=ChangeSerializer(data=request.data)