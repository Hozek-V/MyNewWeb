from django.contrib import admin
from .models import File

# Register your models here.

class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'stl_file', 'gcode_file', 'image', 'printer_name')

admin.site.register(File, FileAdmin)