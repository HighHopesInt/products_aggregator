from django.contrib import admin
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from mptt.admin import DraggableMPTTAdmin

from .models import Category, Product, Brand, Color, Retailer, UploadedFile
from .forms import FileFieldForm


class UploadedFileAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()
        upload_files_urls = [
            path('add/', self.admin_site.admin_view(
                self.multiple_upload_files))
        ]
        return upload_files_urls + urls

    def multiple_upload_files(self, request):
        form = FileFieldForm()
        if request.method == 'POST':
            form = FileFieldForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                files = request.FILES.getlist('file_field')
                for f in files:
                    u = UploadedFile(file=f)
                    u.save()
                return HttpResponseRedirect(
                    reverse('admin:main_uploadedfile_changelist')
                )

        context = dict(
           self.admin_site.each_context(request),
           form=form
        )
        return TemplateResponse(request, "add_multiple_files.html", context)


admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
    ),
    list_display_links=(
        'indented_title',
    ),
)
admin.site.register([Product, Brand, Color, Retailer])
admin.site.register(UploadedFile, UploadedFileAdmin)
