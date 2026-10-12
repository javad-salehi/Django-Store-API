from dataclasses import field, fields
from decimal import Decimal
from itertools import product
from uuid import uuid4
from django.forms.fields import CharField, IntegerField
from rest_framework import serializers
from store.models import Cart, CartItem, Customer, Product , Collection, Review

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