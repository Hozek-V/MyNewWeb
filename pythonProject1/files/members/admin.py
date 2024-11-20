from django.contrib import admin
from .models import Member, File

# Register your models here.

class MemberAdmin(admin.ModelAdmin):
  list_display = ("firstname", "lastname",)

admin.site.register(Member, MemberAdmin)


class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'stl_file', 'gcode_file', 'image', 'printer_name')

admin.site.register(File, FileAdmin)