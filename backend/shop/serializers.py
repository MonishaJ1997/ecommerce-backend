from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Product, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id","name"]



class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(source="category", write_only=True, queryset=Category.objects.all(), required=False)
    image = serializers.ImageField(max_length=None, use_url=True)  # include full URL

    class Meta:
        model = Product
        fields = ["id","name","description","price","image","category","category_id"]

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ["product","quantity"]

class OrderItemCreateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    class Meta:
        model = OrderItem
        fields = ["product","quantity"]

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ["id","items","created_at"]
        read_only_fields = ["id","created_at"]

    def create(self, validated_data):
        items = validated_data.pop("items")
        user = self.context["request"].user
        order = Order.objects.create(user=user)
        order_items = []
        for item in items:
            order_items.append(OrderItem(order=order, product=item["product"], quantity=item.get("quantity",1)))
        OrderItem.objects.bulk_create(order_items)
        return order

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source="orderitem_set", many=True, read_only=True)
    class Meta:
        model = Order
        fields = ["id","user","created_at","items"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","email"]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    class Meta:
        model = User
        fields = ["username","email","password"]

    def create(self, validated_data):
        user = User(username=validated_data["username"], email=validated_data.get("email",""))
        user.set_password(validated_data["password"])
        user.save()
        return user
