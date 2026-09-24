from django.urls import path
from .views import *

urlpatterns = [
    path('',dashboard,name='dashboard'),
    path('command/',send_command,name="send_command")
]