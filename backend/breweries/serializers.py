from rest_framework import serializers
from .models import Brewery


class BrewerySerializer(serializers.ModelSerializer):
    """
    Serializer for the Brewery model.
    """
    class Meta:
        model = Brewery
        fields = [
            'id', 'name', 'brewery_type', 'city', 'state', 
            'country', 'phone', 'website_url'
        ]