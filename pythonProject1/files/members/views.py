from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from .models import Member, File
from .forms import FileUploadForm

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
