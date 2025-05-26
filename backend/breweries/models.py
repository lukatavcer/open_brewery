from django.db import models


class Brewery(models.Model):
    """
    Model representing a brewery.
    Fields match the structure from the Open Brewery DB API.
    """
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=255)
    brewery_type = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    
    # Additional fields that might be useful
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Brewery"
        verbose_name_plural = "Breweries"
        ordering = ["name"]
    
    def __str__(self):
        return self.name