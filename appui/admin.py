from django.contrib import admin
from . models import API_Model,Messages
from django.contrib import admin
from .forms import CustomAdminAuthenticationForm

# Register your models here.
admin.site.register(API_Model)
admin.site.register(Messages)


# Alerts for Django admin panel login system 
admin.site.login_form = CustomAdminAuthenticationForm
