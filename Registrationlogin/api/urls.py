from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from api import views

urlpatterns = [
    path('register/',views.StudentRegister.as_view(),name='register'),
    path('Login/',views.StudentLogin.as_view(),name='login'),
    path('Logout/',views.StudentLogout.as_view(),name='logout'),
    path('profile/',views.UserProfileView.as_view(),name='profile'),
    path('applicationform/',views.StudentApplicationForm.as_view(),name='form'),
    path('List/',views.StudentLeaveList.as_view(),name='leavelist'),
    path('Teachershowlist/',views.TeacherShowLeaveList.as_view(),name='teacherleavelist'),
    path('update-status/<int:id>',views.UpdateApplicationStatus.as_view(),name='status'),
    path('api/token/refresh/',TokenRefreshView.as_view(),name='token_refresh')

]
