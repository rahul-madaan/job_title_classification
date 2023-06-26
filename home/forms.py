from django import forms
from .models import ExcelFile


class ExcelFileUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExcelFileUploadForm, self).__init__(*args, **kwargs)
        self.fields['excel_file'].widget.attrs.update({'accept': '.xlsx'})

    class Meta:
        model = ExcelFile
        fields = ('excel_file',)

class ModelSelectForm(forms.Form):
    MODELS = (
        ('model1', 'Model 1'),
        ('model2', 'Model 2'),
        ('model3', 'Model 3'),
    )
    model_choice = forms.ChoiceField(choices=MODELS, label="Select model")