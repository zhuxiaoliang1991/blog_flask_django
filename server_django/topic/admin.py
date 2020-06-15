from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['title','category','limit','author','created_time']
    list_display_links = ['title']
    search_fields = ['title','category','author']
    list_filter = ['created_time']
    fields = ['title','category','limit','author','created_time','modified_time','content']

