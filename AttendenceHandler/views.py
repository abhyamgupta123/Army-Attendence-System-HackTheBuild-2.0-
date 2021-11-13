from django.shortcuts import render

from .utils import (
    getAttendenceFromString,
    markAttendence,
    writeData,
    readCardData,
    verifyCard,
    getMonth,
    getYear
)

from UsersManager.utils import formatCard
from UsersManager.models import UserProfile

from django.contrib.auth.models import User

import datetime

from .validators import validator
from .models import Attendence
# from .models import 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_200_OK
)


class RecordAttendence(APIView):
    # permsission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print("Place Your card on Scanner!")
        dataString, _uid = readCardData()
        
        profile = UserProfile.objects.filter(uid = str(_uid)).first()
        if profile is None:
            return Response({"error": "This card is Invalid or doesn't belongs to any user."}, status = 501)

        if dataString is None:
            return Response({"error": "Card Not Scanned Sucessfully"}, status = 501)

        if validator(dataString):
            attendence_string = markAttendence(dataString)
            if attendence_string is None:
                return Response({"error": "The Card is Currupted or some Changes has been done by someone"}, status = 404)

            response = writeData(attendence_string)
            if response is None:
                return Response({"error": "Error occureed while marking your attendence Try Again."}, status = 501)
            
            if response == 1:
                _user = profile.user

                startDateString = f"{getYear()}-{getMonth()}-{1}"
                startMonthDate = datetime.datetime.strptime(startDateString, "%Y-%m-%d")

                atten_obj = Attendence.objects.filter(user=_user, month=startMonthDate).first()
                if atten_obj is None:
                    Attendence.objects.create(user=_user, month=startMonthDate, att_string=attendence_string[3:])
                else:
                    atten_obj.att_string = attendence_string[3:]
                    atten_obj.save()

                return Response({"message": "Attendence marked sucessfully!"}, status = HTTP_200_OK)

        else:
            return Response({"error": "The card is not Supported. Please Scan the verified attendence card only."}, status = 401)


class FormatCard(APIView):
    def post(self, request, *args, **kwargs):
        print("Place your card on the Sensor to format it.")
        res = formatCard()
        if res is None:
            print("Card couldn't be formated due to some reason, Please Try Again!")
            return Response({"error": "Card Not Scanned Sucessfully"}, status = 501)

        print("Card formatted Sucessfully")
        return Response({"message": "Card formatted Sucessfully"}, status = 200)

class VerifyCard(APIView):
    def post(self, request, *args, **kwargs):
        print("Place Your card on Scanner!")

        _uid, text = verifyCard()

        if _uid is None:
            return Response({"error": "Card Not Scanned Sucessfully"}, status = 501)

        if validator(text.strip()):
            profile = UserProfile.objects.filter(uid = str(_uid)).first()
            if profile is None:
                return Response({"message": "This card is Invalid or doesn't belongs to any user."}, status = 404)
            
            return Response({"message": "The card belongs to this Organization.",
                             "Username": profile.user.username,
                             "Email": profile.user.email}, status = 200)
    
        else:
            return Response({"error": "The card is not Supported. Please Scan the verified attendence card only."}, status = 401)
    

class CalculateAttendence(APIView):

    def post(self, request, *args, **kwargs):
        print("Place your card on Sensor!")

        text, _uid = readCardData()

        if text is None:
            return Response({"error": "Card Not Scanned Sucessfully"}, status = 501)

        profile = UserProfile.objects.filter(uid = str(_uid)).first()

        atten_obj = getAttendenceFromString(text)

        return Response({"message": "Your attendence is obtained Sucessfully!",
                         "Username": profile.user.username,
                         "Email": profile.user.email,
                         "month": getMonth(),
                         "year": getYear(),
                         "data": atten_obj}, status = 200)


        

