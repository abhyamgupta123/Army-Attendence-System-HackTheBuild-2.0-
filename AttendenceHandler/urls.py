from django.urls import path
from . import views

urlpatterns = [
    path('recordAttendence', views.RecordAttendence.as_view(), name = "attendenceRecording"),
    path('calculateAttendence', views.CalculateAttendence.as_view(), name = "calculateAttendence"),
    path('formatCard', views.FormatCard.as_view(), name = "formatYourCard"),
    path('verifyCard', views.VerifyCard.as_view(), name = "verifyYourCard"),
    # path('login', views.Userlogin.as_view(), name = "loginUser"),
    # path('test', views.Testing.as_view(), name = "loginUser"),
]
