from django import forms


# not working yet,
# see: https://docs.djangoproject.com/en/1.11/topics/http/file-uploads/#uploading-multiple-files

class FileFieldForm(forms.Form):
    file_field = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={'multiple': True}
        )
    )
