from rest_framework.serializers import ModelSerializer
from drf_writable_nested import WritableNestedModelSerializer

from .models import Order, OrderItem


class OrderItemsSerializers(ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ("order",)


class OrderSerializer(WritableNestedModelSerializer, ModelSerializer):
    items = OrderItemsSerializers(many=True)

    class Meta:
        model = Order
        fields = ("user", "is_paid", "created_at", "total_price", "items")
