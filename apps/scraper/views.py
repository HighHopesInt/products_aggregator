from django.shortcuts import render
from .forms import ChoseSiteForm


def chose_site_admin(request):
    form = ChoseSiteForm(request.POST)
    context = {'form': form}
    return render(request, 'scraper/chose_sites.html', context)
