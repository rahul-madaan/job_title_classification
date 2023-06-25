from django.shortcuts import render
from .forms import ExcelFileUploadForm
import os

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


def get_predictions(request):
    if request.method == 'POST':
        form = ExcelFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            # Check if the file is a .xlsx file
            uploaded_file = request.FILES['excel_file']
            filename, file_extension = os.path.splitext(uploaded_file.name)
            if file_extension.lower() == '.xlsx':
                # Rename the file
                new_filename = 'new_name.xlsx'
                os.rename(instance.excel_file.path, os.path.join(os.path.dirname(instance.excel_file.path), new_filename))

                # Add your logic to process the file here
                return render(request, 'success.html')
            else:
                # Handle the case when the file is not a .xlsx file
                instance.delete()
                # messages.error(request, 'Invalid file format. Please upload a .xlsx file.')
    else:
        form = ExcelFileUploadForm()
    return render(request, 'get_predictions.html', {'form': form})
