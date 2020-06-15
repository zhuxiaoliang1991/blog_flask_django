from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','nickname','email']
    fields = ['username','nickname','email','info','sign','avatar']