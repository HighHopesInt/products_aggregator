from django import forms
from apps.scraper.models import Site
from apps.scraper.utils import set_field_html_name


class ChooseSiteForm(forms.Form):
    for site in Site.objects.all():
        locals()['site_' + str(site.id)] = forms.BooleanField(
            label=(site.title + ' (' + site.url[:50] + '...)'),
            required=False, widget=forms.CheckboxInput(attrs={
                'value': site.name_for_crawler,
            })
        )
        set_field_html_name(locals()['site_' + str(site.id)], 'site')
