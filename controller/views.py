from .models import Client, Executor, Order, Rate
from rest_framework import viewsets, permissions, generics
from django.views.decorators.http import require_http_methods
from .serializers import ClientSerializer, ExecutorSerializer, OrderSerializer, RateSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    http_method_names = ['get',]
    permission_classes = [permissions.IsAuthenticated]


class ExecutorViewSet(viewsets.ModelViewSet):
    queryset = Executor.objects.all()
    serializer_class = ExecutorSerializer
    http_method_names = ['get',]
    permission_classes = [permissions.IsAuthenticated]


class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    http_method_names = ['get',]
    permission_classes = [permissions.IsAuthenticated]
