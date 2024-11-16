# forms.py
from django import forms
from .models import File


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'stl_file', 'gcode_file', 'image', 'printer_name']

    def clean(self):
        cleaned_data = super().clean()

        # Pokud je nahrán gcode, název tiskárny je povinný
        gcode_file = cleaned_data.get('gcode_file')
        printer_name = cleaned_data.get('printer_name')

        if gcode_file and not printer_name:
            raise forms.ValidationError("Pokud nahráváte GCODE soubor, musíte zadat název tiskárny.")

        return cleaned_data

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'stl_file', 'image', 'gcode_file', 'printer_name']