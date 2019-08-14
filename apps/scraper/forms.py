from django import forms
from .models import Site


class ChoseSiteForm(forms.Form):
    for site in Site.objects.all():
        locals()['site_' + str(site.id)] = forms.BooleanField(
            label=(site.title + ' (' + site.main_url + site.slug[:10] +
                   '...)'),
            required=False
        )
