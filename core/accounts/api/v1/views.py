from rest_framework.generics import GenericAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from .serializers import RegistrationSerializer, CustomTokenSerializer, ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.api.v1.serializers import CustomTokePairSerializer, ProfileSerializer
from rest_framework.generics import UpdateAPIView
from django.contrib.auth import get_user_model
from accounts.models import Profile
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from mail_templated import EmailMessage
from ..utils import SendEmailThreading
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class RegistrationApiView(GenericAPIView):

    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):

        ser = self.serializer_class(data=request.POST)
        if ser.is_valid():
            ser.save()
            data = {
                'email': ser.validated_data['email']
            }
            user = get_object_or_404(User, email=ser.validated_data['email'])
            token = self.get_tokens_for_user(user)
            message = EmailMessage(
                'email/activation.tpl', {'token': token}, 'adminn@admin.com', to=[ser.validated_data['email']])
            SendEmailThreading(message).start()
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return str(refresh.access_token)


class ObtainAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenSerializer

    def post(self, request, *args, **kwargs):
        ser = self.serializer_class(
            data=request.data, context={'request': request})
        ser.is_valid(raise_exception=True)
        user = ser.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            }
        )


class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.object.get(user=request.user.email).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokePairSerializer


class ChangePasswordView(UpdateAPIView):

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("password1"))
            self.object.save()
            return Response("Success.", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileApiView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


class TestEmail(GenericAPIView):

    def get(self, request, *args, **kwargs):
        self.email = 'admin@admin.com'
        user = get_object_or_404(User, email=self.email)
        token = self.get_tokens_for_user(user)
        message = EmailMessage(
            'email/hello.tpl', {'token': token}, 'adminn@admin.com', to=[self.email])
        SendEmailThreading(message).start()
        return Response({"detail": "sent email"})

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return str(refresh.access_token)


class ActivationApiView(APIView):

    def get(self, request, token, *args, **kwargs):
        print(token)
        # decode > id user
        # object user
        # is_verified true
        # if token not valid 


        # else valid response true
        return Response(token)
