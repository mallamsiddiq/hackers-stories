import django_filters
from .models import Items
from django_filters import rest_framework as drf_filters
class ItemsFilter(django_filters.FilterSet):
    text = django_filters.CharFilter(field_name='text', lookup_expr='icontains')

    class Meta:
        model = Items
        fields = ['type','text']


class ItemsApiFilter(drf_filters.FilterSet):
    text = drf_filters.CharFilter(field_name='text', lookup_expr='icontains')
    class Meta:
        model = Items
        fields = ['text']

