from django.urls import path
from . import views

urlpatterns = [
    path('register', views.UserRegistrationView.as_view(), name = "registerUser"),
    path('deleteUser', views.FormatUser.as_view(), name = "formatuser"),
    path('adminpanel', views.AdminHandler.as_view(), name = "adminpanel"),
    path('backupdatabase', views.BackupDatabase.as_view(), name = "backupDatabase"),
    # path('login', views.Userlogin.as_view(), name = "loginUser"),
    path('test', views.Testing.as_view(), name = "loginUser"),
]
