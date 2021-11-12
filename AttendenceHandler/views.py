from django.shortcuts import render

from .utils import (
    markAttendence, 
    writeData, 
    readCardData
)

from .validators import validator
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
        dataString = readCardData()
        
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
                return Response({"message": "Attendence marked sucessfully!"}, status = HTTP_200_OK)

        else:
            return Response({"error": "The card is not Supported. Please Scan the verified attendence card only."}, status = 401)