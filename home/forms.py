from django import forms
from .models import ExcelFile


class ExcelFileUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExcelFileUploadForm, self).__init__(*args, **kwargs)
        self.fields['excel_file'].widget.attrs.update({'accept': '.xlsx'})

    class Meta:
        model = ExcelFile
        fields = ('excel_file',)
