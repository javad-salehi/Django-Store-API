from dataclasses import field, fields
from decimal import Decimal
from itertools import product
from uuid import uuid4
from .signals import order_created
from django.db import transaction
from rest_framework import serializers
from .models import Cart, CartItem, Customer, Order, OrderItem, Product , Collection, Review

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id' , 'title' , 'products_count']

    products_count = serializers.IntegerField(read_only = True)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id' , 'title' ,'description' , 'slug' , 'inventory' , 'unit_price' , 'price_with_tax' , 'collection']
    #id = serializers.IntegerField()
    #title = serializers.CharField(max_length=255)
    #price = serializers.DecimalField(max_digits=6 , decimal_places=2 , source = 'unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name= 'calculate_tax')
    #collection = serializers.HyperlinkedRelatedField(
    #    queryset = Collection.objects.all() ,
    #    view_name = 'collection-detail'
    #)
    def calculate_tax (self , product : Product) :
        return product.unit_price * Decimal(1.1)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta :
        model = Review
        fields = ['id' , 'date','name' , 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id = product_id , **validated_data)

        
class SimpleProductSerialazer(serializers.ModelSerializer):
    class Meta :
        model = Product
        fields = ['id' , 'title' , 'unit_price']


class CartItemSerialazer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    product = SimpleProductSerialazer(read_only = True)
    class Meta :
        model = CartItem
        fields = ['id' , 'product' , 'quantity' , 'total_price']

    def get_total_price(self,item):
        return item.product.unit_price * item.quantity

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True)
    items = CartItemSerialazer(many = True,read_only = True)
    total_price = serializers.SerializerMethodField()
    class Meta :
        model = Cart
        fields = ['id','items','total_price']
    def get_total_price(self,cart):
        return sum (
            item.product.unit_price * item.quantity
            for item in cart.items.all()
        )


class AddItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self , value) :
        if not Product.objects.filter(pk=value).exists() :
            return serializers.ValidationError('No product with this ID')
        return value
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try :
            #Update quantity of Item
            cart_item = CartItem.objects.get(cart_id = cart_id , product_id = product_id)
            cart_item.quantity += quantity 
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist :
            #Create Item
            self.instance = CartItem.objects.create(cart_id = cart_id , **self.validated_data)
        return self.instance

    class Meta :
        model = CartItem
        fields = ['id' , 'product_id' , 'quantity']

class UpdateCartItemSerializer (serializers.ModelSerializer):
    class Meta :
        model = CartItem
        fields = ['quantity']


class CustomerSerializer (serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta :
        model = Customer
        fields = ['id' , 'user_id' , 'phone' ,'membership' ,'birth_date']



class OrderItemSerializer (serializers.ModelSerializer):
    product = SimpleProductSerialazer(read_only=True)
    class Meta :
        model = OrderItem
        fields = ['id','product','unit_price' , 'quantity'  ]



class OrderSerializer (serializers.ModelSerializer):
    items = OrderItemSerializer(many = True)
    class Meta :
        model = Order
        fields = ['id' , 'customer' , 'placed_at' , 'payment_status' , 'items']


class UpdateOrderSerializer (serializers.ModelSerializer):
    class Meta :
        model = Order
        fields = ['payment_status']

class CreateOrderSerializer (serializers.Serializer):
    cart_id = serializers.UUIDField()
    

    def validate_cart_id (self,cart_id):
        if not Cart.objects.filter(pk = cart_id).exists() :
            raise serializers.ValidationError('No cart with the given cart id')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0 :
            raise serializers.ValidationError('the cart is empty')
        return cart_id
    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']

            customer = Customer.objects.get(user_id = self.context['user_id'])
            order = Order.objects.create(customer = customer)

            cart_items = CartItem.objects\
                                 .select_related('product') \
                                 .filter(cart_id=cart_id)

            order_items = [
                    OrderItem(
                    order = order,
                    product = item.product,
                    quantity = item.quantity,
                    unit_price = item.product.unit_price
                ) for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)
            
            Cart.objects.filter(pk=cart_id).delete()

            order_created.send_robust(self.__class__ , order = order)

            return order




    