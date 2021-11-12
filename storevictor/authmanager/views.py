from django.shortcuts import render
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from .serializers import UserSerializer
from . models import User
from store.models import Client

import jwt, datetime

# Create your views here.

class RegisterView(APIView):
    
    def post(self, request):
        
        serializer = UserSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user_obj = serializer.save()

        #client = Client.objects.get(user__id=user_obj.id, timezone=timezone)
    
        data = serializer.data
        #data["ClientID"] =  client.uuid
     
        return Response(data = data)



class LoginView(APIView):

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')


        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect Password!")

        customer = Client.objects.get(user__id=user.id)

        payload = {
            'id' : user.id,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat' : datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        
        response =  Response(
                { 
                    'full name' : user.get_full_name(),
                    'telephone' :  str(user.telephone.country_code) + str(user.telephone.national_number) ,
                    'email': user.email,
                    'jwt' : token,
                    "uuid" : user.uuid,
                    "clientID" : customer.uuid
                }
            )

        response.set_cookie(key='jwt', value=token, httponly=True)
        return response


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError :
            raise AuthenticationFailed("Unauthenticated")

        user = User.objects.get(id=payload['id'])
        serializer = UserSerializer(user)


        return Response(serializer.data)

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response