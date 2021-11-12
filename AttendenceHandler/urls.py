from django.urls import path
from . import views

urlpatterns = [
    path('recordAttendence', views.UserRegistrationView.as_view(), name = "attendenceRecording"),
    # path('login', views.Userlogin.as_view(), name = "loginUser"),
    # path('test', views.Testing.as_view(), name = "loginUser"),
]
