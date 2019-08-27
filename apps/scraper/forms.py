from django import forms
from apps.scraper.models import Site
from apps.scraper.utils import set_field_html_name


class ChoseSiteForm(forms.Form):
    for site in Site.objects.all():
        locals()['site_' + str(site.id)] = forms.BooleanField(
            label=(site.title + ' (' + site.main_url + site.slug[:10] +
                   '...)'),
            required=False, widget=forms.CheckboxInput(attrs={
                'value': site.name_for_crauler,
            })
        )
        set_field_html_name(locals()['site_' + str(site.id)], 'site')
