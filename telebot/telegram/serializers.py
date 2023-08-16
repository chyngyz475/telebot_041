from rest_framework import serializers
from .models import RetailOrder, WholesaleOrderTelegtam

class WholesaleOrderTelegtamSerializer(serializers.ModelSerializer):
    class Meta:
        model = WholesaleOrderTelegtam
        fields = '__all__'  # Включите здесь все поля, которые вы хотите сериализовать


class RetailOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailOrder
        fields = '__all__'  # Включите здесь все поля, которые вы хотите сериализовать