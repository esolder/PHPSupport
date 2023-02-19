import os
import json

from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
import requests
from dotenv import load_dotenv

from .serializers import ClientSerializer, ExecutorSerializer, OrderSerializer, RateSerializer
from .models import Client, Executor, Order, Rate


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        free = self.request.query_params.get('free', None)
        if free is not None:
            queryset = queryset.filter(executor=None)
        return queryset
    
    def create(self, request, *args, **kwargs):
        client_url = request.data['client']
        client = get_object_or_404(Client, pk=client_url.split('/')[-2])
        if client.subscription_end <= timezone.now().date():
            raise ValidationError("Подписка клиента истекла")
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        rate = Rate.objects.first()
        serializer.save(rate=rate)

    def perform_update(self, serializer):
        order = serializer.save()
        if order.is_complete:
            order.complete_date = timezone.now().date()
        self.send_message_to_client(order)

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        if order.executor is None and 'executor' not in request.data and 'credentials' not in request.data:
            return Response({'detail': 'You cannot modify this order without providing an executor.'},
                            status=status.HTTP_400_BAD_REQUEST)
        if order.is_complete:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        order = self.get_object()
        if order.executor is None and 'executor' not in request.data and 'credentials' not in request.data:
            return Response({'detail': 'You cannot modify this order without providing an executor.'},
                            status=status.HTTP_400_BAD_REQUEST)
        if order.is_complete:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        if order.is_complete:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def send_message_to_client(self, order):
        load_dotenv()
        bot_tokens = {'client': os.environ['CLIENT_BOT_TOKEN'],
                      'executor': os.environ['EXECUTOR_BOT_TOKEN']}
        chat_ids = {'client': order.client_tg_id,
                    'executor': order.executor_tg_id}
        text, bot, reply_markup = self.message_selection(order)
        tg_message_url = f'https://api.telegram.org/bot{bot_tokens[bot]}/sendMessage'
        params = {'chat_id': chat_ids[bot], 
                  'text': text,
                  'reply_markup': reply_markup}
        requests.get(tg_message_url, params=params)

    def message_selection(self, order):
        if order.is_complete:
            reply_markup = self.get_reply_markup('Новый заказ', 'new_order')
            return 'Ваш заказ выполнен', 'client', reply_markup
        if order.is_taken:
            self.send_credentials(order)
            return f'Ваш заказ в процессе выполнения', 'client', ''
        if order.estimate:
            return f'Ваш заказ будет выполнен за {order.estimate}', 'client', ''
        if order.answers:
            return f'Ответы заказчика: {order.answers}', 'executor', ''
        if order.questions:
            reply_markup = self.get_reply_markup('Написать ответы', 'answers')
            return f'Вопросы от разработчика: {order.questions}', 'client', reply_markup
        if order.executor:
            return 'Исполнитель найден', 'client', ''
        if order.credentials:
            return 'Ваши секретные данные будут переданы исполнителю', 'client', ''
        
        
        
    def get_reply_markup(self, text, callback_data):
        reply_markup = {
            'inline_keyboard': [
                [
                    {
                        'text': text, 
                        'callback_data': callback_data
                    }
                ]
            ]
        }
        return json.dumps(reply_markup)

    def send_credentials(self, order): 
        executor_bot_token = os.environ['EXECUTOR_BOT_TOKEN']
        chat_id = order.executor_tg_id
        tg_message_url = f'https://api.telegram.org/bot{executor_bot_token}/sendMessage'
        params = {'chat_id': chat_id, 'text': order.credentials}
        requests.get(tg_message_url, params=params)

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


class ActualRateView(generics.RetrieveAPIView):
    serializer_class = RateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Rate.objects.first()
