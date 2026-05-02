from django.contrib import admin
from .models import CustomUser, Attendance, Noti

admin.site.register(CustomUser)
admin.site.register(Attendance)
admin.site.register(Noti)
from .models import Report
admin.site.register(Report)