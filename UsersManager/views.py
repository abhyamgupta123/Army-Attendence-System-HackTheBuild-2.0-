from django.shortcuts import render

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .utils import (
    readCard, 
    formatCard
)
from .models import UserProfile

import datetime

# for using restframework JWT tocken system
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)


@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationView(APIView):
    # permsission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        login_name = request.data.get('loginName', None)
        email = request.data.get('email', None)
        userPassword = request.data.get('loginpass', None)
        confirmPass = request.data.get('confirmloginpass', None)

        if userPassword == confirmPass:
            if (User.objects.filter(username=login_name).exists()):                 
                # messages.info(request, "Username must be unique", fail_silently=True)
                print("Username must be unique")
                return Response({"error": "Username Must be Unique"}, status = 501)

            elif (User.objects.filter(email=email).exists()):                       
                # messages.info(request, "Email must be unique", fail_silently=True)
                print("Email must be unique")
                return Response({"error": "Email must be unique"}, status = 501)

            else:                                                                   
                if not (userPassword.isalnum()):                                         
                    # messages.info(request, "Password must be alphanumeric", fail_silently=True)
                    print(userPassword)
                    return Response({"error": "Password must be alphanumeric"}, status = 501)

                elif(len(userPassword) <8):                                         
                    # messages.info(request, "Minimum 8 charechters required in Password", fail_silently=True)
                    return Response({"error": "Minimum 8 charechters required in Password"}, status = 501)

                else:                                                               
                    # print("regitsered with {} and {}".format(login_name, userPassword))
                    user = User.objects.create_user(username=login_name, password=userPassword, email=email)

                    # now asking for reading Card
                    print("Place your card on sensor to refister Yourself")
                    res = formatCard()
                    if res is None:
                        return Response({"error": "Card Not Scanned Sucessfully"}, status = 501)

                    _id = readCard()
                    if _id is None:
                        return Response({"error": "Card Not Verified Sucessfully"}, status = 501)
                    
                    if UserProfile.objects.filter(uid=_id).exists():
                        return Response({"error": "User Already Registered with Given Attendence Card"}, status = 501)
                    
                    UserProfile.objects.create(user = user, uid = _id)
                    user.save()
                    print("user created succesfuly")
                    return Response({"message": "User Registered Sucessfully"}, status = HTTP_200_OK)


        else:
            # messages.info(request, "Password Doesn't Matched", fail_silently=True)
            return Response({"error": "Passwords do not match"}, status = 501)


class FormatUser(APIView):

    def delete(self, request, *args, **kwargs):
        login_name = request.data.get('username', None)
        # userPassword = request.data.get('loginpass', None)
        
        user_model = User.objects.filter(username=login_name).first()

        if user_model is None:
            return Response({"error": "User not found with given Username"}, status = 404)

        print("Place your card to delete your data")
        _id = readCard()
        if _id is None:
            return Response({"error": "Card was not placed on Sensor Properly."}, status = 501)

        profile = UserProfile.objects.filter(uid=_id).first()

        if profile is None:
            user_model.delete()

            print("Place your card on sensor to refister Yourself")
            res = formatCard()
            if res is None:
                return Response({"error": "Card Not Scanned Sucessfully"}, status = 501)

            return Response({"message": "This card is not Associated with any user yet."}, status = 200)


        if profile.user.username == login_name:
            user_model.delete()

            print("Place your card on sensor to refister Yourself")
            res = formatCard()
            if res is None:
                return Response({"error": "Card Not Scanned Sucessfully"}, status = 501)

            return Response({"message": "User Deleted Sucessfully."}, status = 200)

        return Response({"error": "Card doesn't match with its owner."}, status = 501)


class Testing(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({"message": "everything is good"}, status = 200)



# @method_decorator(csrf_exempt, name='dispatch')
# class Userlogin(APIView):

#     def post(self, request, *args, **kwargs):
#         username = request.data.get("username")
#         password = request.data.get("password")

#         if username is None or password is None:
#             return Response({'error': 'Please provide both username and password'},
#                             status=HTTP_400_BAD_REQUEST)

#         user = authenticate(username=username, password=password)
#         if not user:
#             return Response({'error': 'Invalid Credentials'},
#                             status=HTTP_404_NOT_FOUND)

#         token, _ = Token.objects.get_or_create(user=user)

#         return Response({'token': token.key},
#                         status=HTTP_200_OK)

# @method_decorator(csrf_exempt, name='dispatch')