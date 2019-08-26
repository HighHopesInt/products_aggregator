from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import ChoseSiteForm
from .util_for_scraping import util


def chose_site_admin(request):
    form = ChoseSiteForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            site_1 = False
            site_2 = False
            if request.POST.get('site_1'):
                site_1 = True
            if request.POST.get('site_2'):
                site_2 = True
            parse = util.crauler.delay(site_1, site_2)
            if not parse.ready():
                messages.warning(request, 'Scraping in progress')
            return HttpResponseRedirect('/admin/main/uploadedfile/')
    context = {'form': form}
    return render(request, 'scraper/chose_sites.html', context)
