from django.shortcuts import render

from rest_framework.decorators import api_view, authentication_classes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from acc.models import Account
from acc.serializers import (
    RegistrationSerializer,
    AccountPropertiesSerializer,
    AccountUpdateSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import RetrieveAPIView


@api_view(['POST', ])
@authentication_classes([])
def registration_view(request):
    data = {}
    email = request.data.get('email', '0').lower()
    try:
        account = Account.objects.get(email=email)
        data['message'] = 'This email is currently occupied.'
        data['response'] = 'Error'
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    except Account.DoesNotExist:
        pass

    username = request.data.get('username', '0')
    try:
        account = Account.objects.get(username=username)
        data['message'] = 'This username is currently occupied.'
        data['response'] = 'Error'
        return Response(data=data, status=status.HTTP_403_FORBIDDEN)
    except Account.DoesNotExist:
        pass

    password = request.data.get('password', '0')
    val = validate_password(password)
    if val[0] is None:
        data['message'] = val[1]
        data['response'] = 'Error'
        return Response(data, status=status.HTTP_403_FORBIDDEN)
    phone_number = request.data.get('number', '0')
    if len(phone_number) != 11:
        data['message'] = "phone number must contain 11 characters."
        data['response'] = 'Error'
        return Response(data, status=status.HTTP_403_FORBIDDEN)

    data = {
        'password': password,
        'email': email,
        'phone_number': request.data.get('number', '0'),
        'username': username
    }
    serializer = RegistrationSerializer(data=data)

    if serializer.is_valid():
        account = serializer.save()
        ser = RegistrationSerializer(account)
        data = ser.data
        token = RefreshToken.for_user(user=account)
        data['userId'] = account.pk
        data['email'] = account.email
        data['username'] = account.username
        data['refresh_token'] = str(token)
        data['access_token'] = str(token.access_token)
        account.save()

        return Response(data=data, status=status.HTTP_200_OK)
    else:
        data = serializer.errors
        return Response(data=data, status=status.HTTP_403_FORBIDDEN)


def validate_password(passwd):
    val = {0: "not None", 1: "not any error"}

    if len(passwd) < 6:
        val[0] = None
        val[1] = 'too short'
        return val
    if len(passwd) > 40:
        val[0] = None
        val[1] = 'too long'
        return val
    if not any(char.isdigit() for char in passwd):
        val[0] = None
        val[1] = 'must contain numbers.'
        return val
    return val


# --- LOGIN VIEWS--

class Login(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        context = {}
        email = request.data.get('username')
        password = request.data.get('password')
        account = authenticate(email=email, password=password)
        if account:
            context['response'] = 'Successfully authenticated.'
            context['pk'] = account.pk
            context['email'] = email.lower()
            context['image'] = str(account.avatar)
            token = RefreshToken.for_user(user=account)
            context['refresh_token'] = str(token)
            context['access_token'] = str(token.access_token)
            return Response(data=context, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'message': 'username or password are wrong.'})



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([JWTAuthentication, ])
def does_account_exist_view(request):
    if request.method == 'GET':
        email = request.GET['email'].lower()
        data = {}
        try:
            Account.objects.get(email=email)
            data['response'] = 'account with email: {email} exists'.format(email=email)
        except Account.DoesNotExist:
            data['response'] = "Account does not exist"
            return Response(data=data, status=status.HTTP_403_FORBIDDEN)
        return Response(data, status=status.HTTP_501_NOT_IMPLEMENTED)

#--SHOW-PROFILE--

@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
def account_properties_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AccountPropertiesSerializer(account)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


# --UPDATE--

@api_view(['PATCH', ])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
def update_account_view(request):
    try:
        account = request.user
        print(account)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        serializer = AccountUpdateSerializer(account, data=request.data, partial=True)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = 'Account update success'
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)