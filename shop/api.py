from django.db.models import Count, Avg, Sum
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Brand, Frame, Review, Order, Customer
from .serializers import BrandSerializer, FrameSerializer, ReviewSerializer


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class FrameViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FrameSerializer

    def get_queryset(self):
        qs = Frame.objects.select_related('brand')
        brand = self.request.query_params.get('brand')
        if brand:
            qs = qs.filter(brand_id=brand)
        return qs


class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (Review.objects.filter(approved=True)
                .select_related('order__customer__user', 'order__frame'))
    serializer_class = ReviewSerializer


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def dashboard_api(request):
    revenue = Order.objects.filter(status='PU').aggregate(s=Sum('price'))['s'] or 0
    return Response({
        'orders': Order.objects.count(),
        'picked_up': Order.objects.filter(status='PU').count(),
        'revenue': float(revenue),
        'customers': Customer.objects.count(),
        'repeat_customers': Customer.objects.annotate(n=Count('orders')).filter(n__gt=1).count(),
        'average_rating': Review.objects.aggregate(a=Avg('rating'))['a'],
        'top_brands': list(Order.objects.exclude(status='CN')
                           .values('frame__brand__name')
                           .annotate(orders=Count('id')).order_by('-orders')[:5]),
    })