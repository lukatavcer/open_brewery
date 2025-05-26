import requests
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Brewery
from .serializers import BrewerySerializer


class BreweryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Brewery instances.
    """
    queryset = Brewery.objects.all()
    serializer_class = BrewerySerializer
    
    @action(detail=False, methods=['get'])
    def fetch_from_api(self, request):
        """
        Fetch breweries from the Open Brewery DB API and save them to the database.
        """
        try:
            # Fetch data from the Open Brewery DB API
            response = requests.get('https://api.openbrewerydb.org/v1/breweries')
            
            if response.status_code != 200:
                return Response(
                    {'error': f'Failed to fetch data from API: {response.status_code}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            breweries_data = response.json()
            
            # Process each brewery
            for brewery_data in breweries_data:
                # Check if brewery already exists
                brewery_id = brewery_data.get('id')
                if brewery_id:
                    brewery, created = Brewery.objects.update_or_create(
                        id=brewery_id,
                        defaults={
                            'name': brewery_data.get('name', ''),
                            'brewery_type': brewery_data.get('brewery_type', ''),
                            'city': brewery_data.get('city', ''),
                            'state': brewery_data.get('state', ''),
                            'country': brewery_data.get('country', ''),
                            'phone': brewery_data.get('phone', ''),
                            'website_url': brewery_data.get('website_url', ''),
                        }
                    )
            
            return Response({'message': f'Successfully imported {len(breweries_data)} breweries'})
            
        except Exception as e:
            return Response(
                {'error': f'An error occurred: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )