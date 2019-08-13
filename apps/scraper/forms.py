from django import forms
from .models import Site


class ChoseSiteForm(forms.Form):
    for site in range(len(Site.objects.all())):
        locals()['site_' + str(site + 1)] = forms.BooleanField(
            label=(Site.objects.get(id=site + 1).title +
                   ' (' + Site.objects.get(id=site + 1).main_url +
                   Site.objects.get(id=site + 1).slug[:20] + '...)'),
            required=False
        )
