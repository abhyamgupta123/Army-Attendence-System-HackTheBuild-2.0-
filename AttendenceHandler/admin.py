from django.contrib import admin
from .models import Attendence


class AttendenceTable(admin.ModelAdmin):
    list_display = ("user", "month", "att_string")

admin.site.register(Attendence, AttendenceTable)