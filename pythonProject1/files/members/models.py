import os
from django.db import models

class File(models.Model):
  # Sloupec pro název modelu
  name = models.CharField(max_length=255)

  # Sloupce pro 3D model (stl nebo 3mf)
  stl_file = models.FileField(upload_to='models/', blank=True, null=True)
  gcode_file = models.FileField(upload_to='gcode/', blank=True, null=True)

  # Volitelný obrázek 3D modelu
  image = models.ImageField(upload_to='images/', blank=True, null=True)

  # Pokud je nahrán gcode, musí být název tiskárny
  printer_name = models.CharField(max_length=255, blank=True, null=True)

  def __str__(self):
    return self.name

  # Metoda pro detekci přípony souboru
  def get_stl_file_extension(self):
    if self.stl_file:
      return os.path.splitext(self.stl_file.name)[1].lower()  # Získáme příponu
    return ""  # Pokud soubor není přítomen, vrátíme prázdný řetězec

  # Metoda pro kontrolu, zda je soubor .stl
  def is_stl(self):
    return self.get_stl_file_extension() == '.stl'

  # Metoda pro kontrolu, zda je soubor .3mf
  def is_3mf(self):
    return self.get_stl_file_extension() == '.3mf'
