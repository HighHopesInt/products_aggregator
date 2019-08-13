from django import forms


class ChoseSiteForm(forms.Form):
    site_one = forms.BooleanField(required=False,
                                  label='https://www.francosarto.com/en-US')
    site_two = forms.BooleanField(required=False,
                                  label=('https://www.saksfifthavenue.com'
                                         '/Men/Shoes'))
