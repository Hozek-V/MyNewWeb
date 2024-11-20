from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('files/', files, name='files'),
    path('about/', about, name='about'),
    path('upload/', upload_file, name='upload_file'),
    path('file/<int:id>/', file_detail, name='file_detail'),
    path('file/<int:id>/edit/', file_edit, name='edit_file'),
    path('file/<int:id>/delete/', file_delete, name='delete_file'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)