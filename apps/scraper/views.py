from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import ChoseSiteForm
from .util_for_scraping import util


def chose_site_admin(request):
    form = ChoseSiteForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            not_chose_site = True
            if request.POST.get('site_1'):
                util.crauler_saks(request)
                not_chose_site = False
            if request.POST.get('site_2', ''):
                util.crauler_fran(request)
                not_chose_site = False
            if not_chose_site:
                messages.error(request, 'You don\' chose site')
            return HttpResponseRedirect('/admin/main/uploadedfile/')
    context = {'form': form}
    return render(request, 'scraper/chose_sites.html', context)
