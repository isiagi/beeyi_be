from django.http import QueryDict
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth.models import User
from rest_framework.response import Response
from .serializers import UserSerializer, EmailSerializer, ResetPasswordSerializer, PasswordSerializer, MemberSerializer, SignSerializer
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView

from .email_service import send

import random
import string
from datetime import datetime
from .models import CustomUser

from django.db.models import Sum

from rest_framework.permissions import AllowAny
import string
# from django_filters.rest_framework import DjangoFilterBackend

    
class UserDetailApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    permission_classes = [AllowAny]

    # def get_queryset(self):
    #     return CustomUser.objects.filter(id=self.kwargs['pk'])
    
    def update(self, request, *args, **kwargs):
        print("Request data:", request.data)
        return super().update(request, *args, **kwargs)

    # def get_object(self):
    #     print(f"Requested PK: {self.kwargs.get('pk')}")
    #     obj = super().get_object()
    #     print(f"Retrieved object ID: {obj.id}")
    #     return obj

class UserDeleteApi(DestroyAPIView):
   queryset = CustomUser.objects.all()
   serializer_class = UserSerializer

# Login View

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    # Get user by pass in username or return 404
    user = get_object_or_404(CustomUser, username=request.data['username'])

    # Check if password provided and in database match
    if not user.check_password(request.data['password']):
        return Response({"message": "Invalid Username or Password"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Get or create token
    token, created = Token.objects.get_or_create(user=user)

    # serializer data sent by user
    serializer = UserSerializer(instance=user)

    # Respond with status of 200 with Token and user data
    return Response({'Token': token.key, 'User': serializer.data})



# Sign Up

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    # serialize data sent by user
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        # save data to database
        serializer.save()

        # Fetch save user by username from database and hash password
        user = CustomUser.objects.get(username=request.data.get('username'))
        user.set_password(request.data.get('password'))
        user.save()

        # Create token for user
        token = Token.objects.create(user=user)

        # Respond with status of 200 with Token and user data
        return Response({'Token': token.key, 'User': serializer.data}, status=status.HTTP_201_CREATED)
    
    # Throw errors if serialization of data failed
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Logout
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    # delete token
    request.user.auth_token.delete()

    # Response
    return Response({"message": "User Logged Out"}, status=status.HTTP_200_OK)





@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    # Deserialize request data,
    serializer = EmailSerializer(data=request.data)

    # Check if data is valid, matching the model / serializer requirements
    serializer.is_valid(raise_exception=True)

    # Access the email from pass data from the request
    email = request.data['email']

    print("email", email)
    
    # Find the first entry of the email from the user table
    user = CustomUser.objects.filter(email=email).first()

    if user:
        # Make encrptyed text for the user id
        encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))

        # Generate Token with user object
        token = PasswordResetTokenGenerator().make_token(user)

        # User reverse to get url path of url with name 'reset_password' in url file
        # And passing some data along matching the url

        reset_url = reverse('reset_password', kwargs={'encoded_pk': encoded_pk, 'token': token})

        # Make reset Link
        reset_link = f"http://127.0.0.1:8000{reset_url}"

        # Send reset link by email.
        send('Reset Password Link', reset_link, [email])

        return Response({"message": "Password reset link sent to your email"}, status=status.HTTP_200_OK)
    
    return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
def reset_password(request, *args, **kwargs):
    # Deserialize request data,
    serializer = ResetPasswordSerializer(data=request.data, context={'kwargs': kwargs})

      # Check if data is valid
    serializer.is_valid(raise_exception=True)

    return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
    
