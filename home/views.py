from django.shortcuts import render, redirect
from .forms import ExcelFileUploadForm
from django.http import FileResponse
from django.contrib import messages
import os
import glob
from classifier.model import prediction


# Create your views here.

def index(request):
    return render(request, 'index.html')


def upload_excel(request):
    if request.method == 'POST':
        files = glob.glob('uploaded_files/*')
        for f in files:
            os.remove(f)
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
                os.rename(instance.excel_file.path,
                          os.path.join(os.path.dirname(instance.excel_file.path), new_filename))
                messages.add_message(request, messages.SUCCESS, 'Excel file uploaded successfully')
                # Add your logic to process the file here
                return render(request, 'get_predictions.html')
            else:
                # Handle the case when the file is not a .xlsx file
                instance.delete()
                messages.error(request, 'Invalid file format. Please upload a .xlsx file.')
    else:
        form = ExcelFileUploadForm()
    return render(request, 'get_predictions.html', {'form': form})


def download_excel(request):
    file_path = 'output_files/output.xlsx'
    response = FileResponse(open(file_path, 'rb'),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{file_path.split("/")[-1]}"'
    # messages.add_message(request, messages.SUCCESS, 'Excel file downloaded successfully')
    return response


def button_view(request):
    if request.method == "POST":
        # Add your button functionality here.
        # display the message
        messages.success(request, 'Button pressed successfully!')
        return redirect("train_model")
    return render(request, 'train_model.html')


def run_model(request):
    response = prediction("sales head")
    messages.add_message(request, messages.SUCCESS, response)
    return render(request, 'get_predictions.html')
