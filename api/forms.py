import os

from django import forms


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)

        for file in result:
            if not file.name.endswith('.m4a'):
                raise forms.ValidationError("Only .mp4 files are allowed.")

        return result


class MultiFileFieldForm(forms.Form):
    file_field = MultipleFileField()


# sheet

class UploadSheetForm(forms.Form):
    cell_range_start = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'A11'}))
    cell_range_stop = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'F318'}))
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            ext = os.path.splitext(file.name)[1]
            if ext.lower() != '.xlsx':
                raise forms.ValidationError('Only .xlsx files are allowed.')

        return file

