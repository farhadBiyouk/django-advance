from django.urls import path
from . import views
# from rest_framework.authtoken.views import ObtainAuthToken\
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

app_name = 'api-v1'
urlpatterns = [
    path('registration/', views.RegistrationApiView.as_view(),
         name='registration-user'),
    path('token/login/', views.ObtainAuthToken.as_view(), name='token-login'),
    path('token/logout/', views.CustomDiscardAuthToken.as_view(), name='token-logout'),


    # change password

    path('change-password/', views.ChangePasswordView.as_view(), name='password_change'),

    path('jwt/create/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # profile
    path('profile/', views.ProfileApiView.as_view(),name='profile'),
]
