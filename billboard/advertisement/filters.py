from django.forms import DateTimeInput
from django_filters import FilterSet, NumberFilter, ModelChoiceFilter, DateTimeFilter, CharFilter
from .models import Advertisement, Category



class AdvertisementSearchFilter(FilterSet):
   
   
    category = ModelChoiceFilter(queryset=Category.objects.all())
    creation_date = DateTimeFilter(
            lookup_expr='gt', 
            widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ))
    find = CharFilter(lookup_expr='icontains')
            
    
        