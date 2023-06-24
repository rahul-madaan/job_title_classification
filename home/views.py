from django.shortcuts import render
from .forms import ExcelFileUploadForm


# Create your views here.

def index(request):
    return render(request, 'index.html')


def upload_excel(request):
    if request.method == 'POST':
        form = ExcelFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            # Add your logic to process the file here
            return render(request, 'success.html')
    else:
        form = ExcelFileUploadForm()
    return render(request, 'upload.html', {'form': form})


def train_model(request):
    return render(request, 'train_model.html')
