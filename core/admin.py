from django.contrib import admin
from .models import User, EmployeeProfile, Attachment
from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)
admin.site.register(EmployeeProfile)
admin.site.register(Attachment)
