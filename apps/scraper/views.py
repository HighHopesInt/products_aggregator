from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect

from apps.scraper.forms import ChoseSiteForm
from apps.scraper import tasks


def chose_site_admin(request):
    form = ChoseSiteForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            sites = request.POST.getlist('site')
            if sites:
                parse = tasks.crauler.delay(sites)
                if not parse.ready():
                    messages.warning(request, 'Scraping in progress')
            else:
                messages.error(request, 'You don\'t choice site')
            return HttpResponseRedirect('/admin/main/uploadedfile/')
    context = {'form': form}
    return render(request, 'scraper/chose_sites.html', context)
