# from django.contrib import admin
# from django.urls import path,include
# from rest_framework.routers import DefaultRouter
# from api import views
# from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView

# router=DefaultRouter()
# # Register Router in Viewset
# router.register('Register',views.StudentRegister,basename='register')
# router.register('Login',views.StudentLogin,basename='login')


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include(router.urls)),
#     path('gettoken/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
#     path('refreshtoken/',TokenRefreshView.as_view(),name='token_refresh'),
#     path('verifytoken/',TokenVerifyView.as_view(),name='token_verify'),    

# ]


from django.urls import path,include
from api import views

urlpatterns = [
    path('register/',views.StudentRegister.as_view(),name='register'),
    path('Login/',views.StudentLogin.as_view(),name='login'),

]
