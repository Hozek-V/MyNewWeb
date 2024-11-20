import os
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .models import *
from .forms import *


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrace byla úspěšná! Nyní se můžete přihlásit.')
            return redirect('home')  # Přesměrování na přihlášení po úspěšné registraci
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})


def home(request):
  return render(request,'home.html')

def about(request):
  return render(request,'about.html')

def files(request):
  files = File.objects.all()
  return render(request, 'files.html', {'files': files})


def upload_file(request):
  if request.method == 'POST':
    form = FileUploadForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      return redirect('files')  # Po úspěšném nahrání přesměrujeme na seznam souborů
    else:
      return render(request, 'upload_file.html', {'form': form})
  else:
    form = FileUploadForm()
  return render(request, 'upload_file.html', {'form': form})

def file_detail(request, id):
  file = get_object_or_404(File, id=id)
  return render(request, 'file_detail.html', {'file': file})


def file_edit(request, id):
    # Načteme soubor podle ID
    file = get_object_or_404(File, id=id)

    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES, instance=file)

        if form.is_valid():
            print("Formulář je validní")  # Log pro ladění
            print("Nahraný soubor:", request.FILES.get('file'))  # Zobrazení nahraného souboru
            """
            # Před uložením nových souborů smažeme staré soubory, pokud byly změněny
            if 'stl_file' in request.FILES:
                if file.stl_file:
                    try:
                        print(f"Mažu starý STL soubor: {file.stl_file.name}")
                        file.stl_file.delete(save=False)  # Mažeme starý soubor
                    except Exception as e:
                        print(f"Chyba při mazání starého STL souboru: {e}")
                file.stl_file = request.FILES['stl_file']

            if 'image' in request.FILES:
                if file.image:
                    try:
                        print(f"Mažu starý obrázek: {file.image.name}")
                        file.image.delete(save=False)  # Mažeme starý obrázek
                    except Exception as e:
                        print(f"Chyba při mazání starého obrázku: {e}")
                file.image = request.FILES['image']

            if 'gcode_file' in request.FILES:
                if file.gcode_file:
                    try:
                        print(f"Mažu starý Gcode soubor: {file.gcode_file.name}")
                        file.gcode_file.delete(save=False)  # Mažeme starý Gcode soubor
                    except Exception as e:
                        print(f"Chyba při mazání starého Gcode souboru: {e}")
                file.gcode_file = request.FILES['gcode_file']
            """
            # Uložení změn do databáze
            form.save()

            return redirect('file_detail', id=file.id)  # Po úspěšné editaci přesměrujeme na detail souboru

        else:
            print("Formulář není validní")  # Log pro ladění
            print("Chyby ve formuláři:", form.errors)  # Výpis chyb formuláře

    else:
        # Pokud je požadavek GET, zobrazíme formulář s aktuálními daty
        form = FileForm(instance=file)

    return render(request, 'file_edit.html', {'form': form, 'file': file})


def file_delete(request, id):
  # Načteme soubor podle ID
  file = get_object_or_404(File, id=id)

  # Pokud je požadavek POST, smažeme soubor a jeho související soubory
  if request.method == 'POST':
    # Smazání souvisejících souborů (STL, obrázek, Gcode)
    if file.stl_file:
        file.stl_file.delete()
    if file.image:
        file.image.delete()
    if file.gcode_file:
        file.gcode_file.delete()

    # Smazání souboru z databáze
    file.delete()
    return redirect('files')  # Přesměrování na seznam souborů

  # Pokud je požadavek GET, zobrazíme potvrzení smazání
  return render(request, 'file_delete.html', {'file': file})