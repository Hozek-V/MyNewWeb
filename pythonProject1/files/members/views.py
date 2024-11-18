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

def members(request):
  mymembers = Member.objects.all().values()
  template = loader.get_template('members.html')
  context = {
    'mymembers': mymembers,
  }
  return HttpResponse(template.render(context, request))

def home(request):
  return render(request,'home.html')

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
            # Před uložením nových souborů smažeme staré soubory, pokud byly změněny
            if 'stl_file' in request.FILES and file.stl_file:
                # Smazání starého STL souboru
                file.stl_file.delete(save=False)
            if 'image' in request.FILES and file.image:
                # Smazání starého obrázku
                file.image.delete(save=False)
            if 'gcode_file' in request.FILES and file.gcode_file:
                # Smazání starého Gcode souboru
                file.gcode_file.delete(save=False)

            # Uložíme změny do databáze
            form.save()

            return redirect('file_detail', id=file.id)  # Po úspěšné editaci přesměrujeme na detail souboru
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