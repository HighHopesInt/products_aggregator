from django.contrib import admin
from .models import Site


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('title', 'main_url', 'slug')
    search_fields = ('title', )

    def has_add_permission(self, request):
        return False
