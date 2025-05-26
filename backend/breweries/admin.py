from django.contrib import admin
from .models import Brewery


@admin.register(Brewery)
class BreweryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Brewery model.
    """
    list_display = ('name', 'brewery_type', 'city', 'state', 'country')
    list_filter = ('brewery_type', 'state', 'country')
    search_fields = ('name', 'city', 'state')
    readonly_fields = ('id', 'created_at', 'updated_at')