from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import ChoseSiteForm
from .models import Site


def chose_site_admin(request):
    form = ChoseSiteForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            # Next two messages is debug information and don't hit in final
            # version
            for site in Site.objects.all():
                messages.success(request, str(request.POST.get(
                    'site_' + str(site.id), 'False'
                )))
            return HttpResponseRedirect('/admin/main/uploadedfile/')
    context = {'form': form}
    return render(request, 'scraper/chose_sites.html', context)
