from .serializers import StudentSerializer,StudentLoginSerializer,UserProfileSerializer,StudentApplicationSerializer,StudentLeaveListSerializer,TeacherShowStudentList,StatusSerializer
from .models import ApplicationForm
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class StudentRegister(APIView):
    def post(self, request, format=None):
        try:
            serializer = StudentSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'msg': 'Registration Success.'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StudentLogin(APIView):       
    def post(self, request, format=None):
        try:
            serializer = StudentLoginSerializer(data=request.data)
            print('serializer: ', serializer)

            if serializer.is_valid(raise_exception=True):  # Corrected indentation
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']
                
                user = authenticate(username=username, password=password)
                
                if user is not None:
                    token = get_tokens_for_user(user)
                    return Response({'token': token, 'msg': 'Login Successfully!'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class StudentLogout(APIView):
    permission_classes = [permissions.IsAuthenticated]  

    def post(self, request):
        try:
            print(request.data,"::::::::::::::::::::::::::::::")
            refresh_token = request.data.get("refresh")  # Fix: Correct way to access refresh token
            
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token) 
            token.blacklist()  
            
            return Response({"msg": "Logged out successfully!"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            serializer = UserProfileSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class StudentApplicationForm(APIView):
    permission_classes = [IsAuthenticated]  

    def post(self, request):
        try:
            data = request.data.copy()  
            data['user'] = request.user.id  

            serializer = StudentApplicationSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"msg": "Application submitted successfully!"}, status=status.HTTP_201_CREATED)

            return Response({"error": "Invalid data", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentLeaveList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            applications = ApplicationForm.objects.filter(user=request.user) 
            print('user: ', request.user)

            if not applications.exists():
                return Response({"error": "No applications found for this user."}, status=status.HTTP_404_NOT_FOUND)

            serializer = StudentLeaveListSerializer(applications, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TeacherShowLeaveList(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request, format=None):
        try:
            if request.user.role != 'teacher':
                return Response({"error": "Only teachers can view this data."}, status=status.HTTP_400_BAD_REQUEST)

            applications = ApplicationForm.objects.all()  
            
            if not applications.exists():
                return Response({"error": "No student leave applications found."}, status=status.HTTP_404_NOT_FOUND)

            serializer = TeacherShowStudentList(applications, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
                    return Response({"error": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    


class UpdateApplicationStatus(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        try:
            application = get_object_or_404(ApplicationForm, id=id)

            # Ensure only teachers can update application status
            if not hasattr(request.user, 'role') or request.user.role != 'teacher':
                return Response({"error": "Only teachers can update application status."}, status=status.HTTP_403_FORBIDDEN)

            new_status = request.data.get("status")
            if not new_status:
                return Response({"error": "Status field is required"}, status=status.HTTP_400_BAD_REQUEST)

            application.status = new_status  
            application.save() 

            return Response({
                "message": "Status updated successfully!",
                "application_id": application.id,
                "status": application.status
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
