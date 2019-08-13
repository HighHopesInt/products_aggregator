from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ChoseSiteForm


def chose_site_admin(request):
    form = ChoseSiteForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            return HttpResponseRedirect('/admin/main/uploadedfile/')
    context = {'form': form}
    return render(request, 'scraper/chose_sites.html', context)
