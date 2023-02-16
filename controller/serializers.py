from .models import Client, Executor, Order, Rate
from rest_framework import serializers

class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'username', 'subscription_end']

    
class ExecutorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Executor
        fields = ['id', 'username']


class RateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rate
        fields = ['id', 'rate', 'when_set']


class OrderSerializer(serializers.ModelSerializer):
    client = serializers.HyperlinkedRelatedField(view_name='clients-detail',
                                                 queryset=Client.objects.all())
    rate = serializers.HyperlinkedRelatedField(view_name='rates-detail',
                                               queryset=Rate.objects.all())
    executor = serializers.HyperlinkedRelatedField(view_name='executors-detail',
                                                   queryset=Executor.objects.all())
    class Meta:
        model = Order
        fields = ['id',
                  'client',
                  'executor',
                  'is_booked',
                  'is_taken',
                  'is_complete',
                  'rate',
                  'estimate',
                  'complete_date']