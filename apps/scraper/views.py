from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import ChoseSiteForm
from .util_for_scraping import save_to_csv, scraper_for_saks


def chose_site_admin(request):
    form = ChoseSiteForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            # Next two messages is debug information and don't hit in final
            # version
            first_site = scraper_for_saks.scraper_saks(request)
            save_to_csv.save_to_csv(first_site, 'shoes.csv')
            messages.success(request, 'Done write')
            return HttpResponseRedirect('/admin/main/uploadedfile/')
    context = {'form': form}
    return render(request, 'scraper/chose_sites.html', context)
