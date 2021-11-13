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
from AttendenceHandler.utils import getAttendenceFromString
from AttendenceHandler.models import Attendence

import datetime
import json

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
            print("Place your card on sensor to refister Yourself")
            res = formatCard()
            if res is None:
                return Response({"error": "Card Not Scanned Sucessfully"}, status = 501)

            user_model.delete()

            return Response({"message": "This card is not Associated with any user yet."}, status = 200)


        if profile.user.username == login_name:
            print("Place your card on sensor to refister Yourself")
            res = formatCard()
            if res is None:
                return Response({"error": "Card Not Scanned Sucessfully"}, status = 501)

            user_model.delete()

            return Response({"message": "User Deleted Sucessfully."}, status = 200)

        return Response({"error": "Card doesn't match with its owner."}, status = 501)


class Testing(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({"message": "everything is good"}, status = 200)


class AdminHandler(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        _user = request.user

        if _user.is_superuser:
            profiles = UserProfile.objects.all()

            data = {}
            for profile in profiles:
                _uid = profile.uid
                atten_objs_for_single_user = Attendence.objects.filter(user = profile.user)
                atten_for_user = {}
                for all_atten in atten_objs_for_single_user:
                    attendences_of_month = getAttendenceFromString(all_atten.att_string)
                    atten_for_user[str(all_atten.month)] = attendences_of_month

                data[profile.user.username] = atten_for_user
            
            return Response({"message": "Data Recieved Sucessfully", 
                             "admin":True,
                             "username": _user.username,
                             "data": data}, status = 200)

        else:
            user_profile = UserProfile.objects.filter(user = _user).first()

            if user_profile is None:
                return Response({"error": "User not found or session exprired!"}, status = 404)

            atten_for_user = {}
            atten_objs_for_single_user = Attendence.objects.filter(user = user_profile.user)
            for all_atten in atten_objs_for_single_user:
                attendences_of_month = getAttendenceFromString(all_atten.att_string)
                atten_for_user[str(all_atten.month)] = attendences_of_month

            return Response({"message": "Data Recieved Sucessfully", 
                             "admin":False,
                             "username": _user.username,
                             "data": atten_for_user}, status = 200)

    
class BackupDatabase(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        _user = request.user

        if _user.is_superuser:
            profiles = UserProfile.objects.all()

            data = {}
            for profile in profiles:
                _uid = profile.uid
                atten_objs_for_single_user = Attendence.objects.filter(user = profile.user)
                atten_for_user = {}
                for all_atten in atten_objs_for_single_user:
                    attendences_of_month = getAttendenceFromString(all_atten.att_string)
                    atten_for_user[str(all_atten.month)] = attendences_of_month

                data[profile.user.username] = atten_for_user

            filename = str(datetime.datetime.today().strftime("%Y-%m-%d")) + ".json"

            with open("BACKUPS/"+filename, "w") as outfile:
                json.dump(data, outfile)
            
            return Response({"message": "Data Backed-Up Sucessfully"}, 
                             status = 200)

        else:
            return Response({"message": "You do not have required Credential to perform this action."}, status = 404)



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