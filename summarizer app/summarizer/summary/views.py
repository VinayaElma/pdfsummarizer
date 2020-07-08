from subprocess import Popen, PIPE,STDOUT
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Document
from .forms import DocumentForm


# Create your views here.

def home(request):
    return render(request, 'home.html')

def form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            filename = request.FILES['document'].name
            #print(filename)
            #summarytext=sumy_summarize.sumy_sum('cogPsych.pdf')
            process = Popen(['python','media/sumy_summarize.py',str(filename)], stdout=PIPE, stderr=STDOUT)
            summarytext = process.stdout.read()
            summary = str(summarytext, 'utf-8')
            #print(summary)
            #print(document.id)
            doc = Document.objects.get(pk=document.id)
            doc.delete()
            return render(request, 'form_summary.html', {'summarytext': summary})
    else:
        form = DocumentForm()
    return render(request, 'model_form_upload.html', {
        'form': form
    })