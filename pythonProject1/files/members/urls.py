from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('files/', files, name='files'),
    path('upload/', upload_file, name='upload_file'),
    path('members/', members, name='members'),
]