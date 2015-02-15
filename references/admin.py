from django.contrib import admin
from references.models import Reference


class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    list_display_links = ('url',)


admin.site.register(Reference, ReferenceAdmin)
