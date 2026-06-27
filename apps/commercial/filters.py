import django_filters

from apps.commercial.models import Order, SupportTicket


class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = ['user', 'status', 'coupon']


class SupportTicketFilter(django_filters.FilterSet):
    class Meta:
        model = SupportTicket
        fields = ['user', 'status']
