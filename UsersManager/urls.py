from django.urls import path
from . import views

urlpatterns = [
    path('register', views.UserRegistrationView.as_view(), name = "registerUser"),
    # path('login', views.Userlogin.as_view(), name = "loginUser"),
    path('deleteUser', views.FormatUser.as_view(), name = "formatuser"),
    path('test', views.Testing.as_view(), name = "loginUser"),
]
