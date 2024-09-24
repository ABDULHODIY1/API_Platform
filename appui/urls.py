from django.urls import path
from .views import *

urlpatterns = [
    path('',Message.as_view(), name='home'),
    path('show',Show.as_view(), name='show'),
]