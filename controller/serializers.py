from .models import Client, Executor, Order, Rate
from rest_framework import serializers

class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = ['username', 'subscription_end']

    
class ExecutorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Executor
        fields = ['username',]


class RateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rate
        fields = ['rate', 'when_set']


class OrderSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    rate = serializers.DecimalField(source='rate.rate', max_digits=10, decimal_places=2)
    executor = ExecutorSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['client',
                  'executor',
                  'is_booked',
                  'is_taken',
                  'is_complete',
                  'rate',
                  'estimate',
                  'complete_date']