from django.db import models

class Member(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  email = models.EmailField(null=True)

  def __str__(self):
    return f"{self.firstname} {self.lastname}"

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