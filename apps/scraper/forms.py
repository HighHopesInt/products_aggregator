from django import forms


class ChoseSiteForm(forms.Form):
    site_one = forms.BooleanField(required=False)
    site_two = forms.BooleanField(required=False)
