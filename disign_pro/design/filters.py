import django_filters

from .models import Order


class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        exclude = ('name', 'title', 'description', 'photo', 'category', 'time_create', 'comment', 'photo_design')


class AdminOrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        exclude = ('title', 'description', 'photo', 'name', 'status', 'time_create', 'comment', 'photo_design')
