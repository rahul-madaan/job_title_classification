import pandas as pd
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
    if request.method == 'POST' and request.POST.get('form_name') == 'upload_training_data':
        files = glob.glob('uploaded_files/training/*')
        for f in files:
            os.remove(f)
        form = ExcelFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            # Check if the file is a .xlsx file
            uploaded_file = request.FILES['excel_file']
            filename, file_extension = os.path.splitext(uploaded_file.name)
            if file_extension.lower() == '.xlsx':
                # Rename the file
                new_filename = 'training_data.xlsx'
                os.rename(instance.excel_file.path,
                          os.path.join(os.path.dirname(instance.excel_file.path),'training' ,new_filename))
                messages.add_message(request, messages.SUCCESS, 'Excel file uploaded successfully')
                # Add your logic to process the file here
                return render(request, 'train_model.html')
            else:
                # Handle the case when the file is not a .xlsx file
                instance.delete()
                messages.error(request, 'Invalid file format. Please upload a .xlsx file.')
    else:
        form = ExcelFileUploadForm()
    return render(request, 'train_model.html', {'form': form})


def get_predictions(request):
    if request.method == 'POST' and request.POST.get('form_name') == 'run_model':
        response = run_model(request)
        return response

    if request.method == 'POST' and request.POST.get('form_name') == 'run_model_single':
        if request.POST.get('job_title') == "":
            messages.add_message(request, messages.WARNING, "Job Title cannot be empty!")
        else:
            job_title = request.POST.get('job_title')
            industry = prediction([job_title])
            return render(request, 'get_predictions.html', {'predicted_industry': industry[0]})

    if request.method == 'POST' and request.POST.get('form_name') == 'upload_excel':
        files = glob.glob('uploaded_files/*')
        for f in files:
            os.remove(f)
        form = ExcelFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            # Check if the file is a .xlsx file
            uploaded_file = request.FILES['excel_file']
            filename, file_extension = os.path.splitext(uploaded_file.name)
            if file_extension.lower() == '.xlsx':
                # Rename the file
                new_filename = 'input.xlsx'
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
    input_df = pd.read_excel("uploaded_files/input.xlsx")
    list(input_df['job title'])

    # open excel, copy first column(job title) and send in predict function.
    industries = prediction(input_df['job title'])
    print(industries)

    industry_df = pd.DataFrame(industries, columns=['industry'])
    result_df = pd.concat([input_df['job title'], industry_df['industry']], axis=1)
    result_df.to_excel("output_files/output.xlsx", index=False)
    messages.add_message(request, messages.SUCCESS, "Output ready to be downloaded!")
    return render(request, 'get_predictions.html')


def run_model_single(request):
    if request.method == "POST":
        job_title = request.POST.get('job_title')
        industry = prediction([job_title])
        return render(request, 'get_predictions.html', {'predicted_industry': industry[0]})
    else:
        return render(request, 'get_predictions.html')
