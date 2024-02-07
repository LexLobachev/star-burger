from rest_framework import serializers
from foodcartapp.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True, allow_empty=False)

    class Meta:
        model = Order
        fields = ['products', 'firstname', 'lastname', 'phonenumber', 'address']

    def create(self, validated_data):
        order = Order.objects.create(firstname=validated_data['firstname'],
                                     lastname=validated_data['lastname'],
                                     phonenumber=validated_data['phonenumber'],
                                     address=validated_data['address'])
        order_items_fields = validated_data['products']
        order_items = [OrderItem(order=order, price=fields.get('product').price * fields.get('quantity'), **fields)
                       for fields in order_items_fields]
        OrderItem.objects.bulk_create(order_items)
        return order
