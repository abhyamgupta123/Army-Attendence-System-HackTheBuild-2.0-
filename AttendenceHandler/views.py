from django.shortcuts import render

# from .utils import 
# from .models import 


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)


class RecordAttendence(APIView):
    # permsission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        