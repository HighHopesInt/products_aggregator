from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import ChoseSiteForm


def chose_site_admin(request):
    form = ChoseSiteForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            # Next two messages is debug information and don't hit in final
            # version
            messages.success(request, str(request.POST.get('site_one',
                                                           'False')))
            messages.success(request, str(request.POST.get('site_two',
                                                           'False')))
            return HttpResponseRedirect('/admin/main/uploadedfile/')
    context = {'form': form}
    return render(request, 'scraper/chose_sites.html', context)
