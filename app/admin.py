from django.contrib import admin

# Register your models here.
from app.models import *

class cust(admin.ModelAdmin):
    list_display = ['username','address','profile_pic']

admin.site.register(Profile,cust)