from .models import Client, Executor, Order, Rate
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
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


class ClientView(generics.RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        username = request.query_params.get('username')
        if username is not None:
            try:
                client = self.queryset.get(username=username)
                serializer = self.serializer_class(client)
                return Response(serializer.data)
            except Client.DoesNotExist:
                pass
        return Response({})


class ExecutorViewSet(viewsets.ModelViewSet):
    queryset = Executor.objects.all()
    serializer_class = ExecutorSerializer
    http_method_names = ['get',]
    permission_classes = [permissions.IsAuthenticated]


class ExecutorView(generics.RetrieveAPIView):
    queryset = Executor.objects.all()
    serializer_class = ExecutorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        username = request.query_params.get('username')
        if username is not None:
            try:
                executor = self.queryset.get(username=username)
                serializer = self.serializer_class(executor)
                return Response(serializer.data)
            except Executor.DoesNotExist:
                pass
        return Response({})



class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    http_method_names = ['get',]
    permission_classes = [permissions.IsAuthenticated]


class LastRateView(generics.RetrieveAPIView):
    serializer_class = RateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Rate.objects.first()
