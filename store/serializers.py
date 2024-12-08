from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, Product, Order




class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = [ 'id',"username", "email", "password", "password_confirm"]
        read_only_fields = ["id"]

    def validate(self, data):
        # if '_'in data["username"]:
        #     raise serializers.ValidationError("_ should not in username")
        
        # if "id" in self.initial_data:
        #     raise serializers.ValidationError("ID field must not be included in the registration request.")
        
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        print(data)
        print(type(data))
        
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        print(type(self.initial_data))

        
        
        # if "id" in data['id']:
        #     raise serializers.ValidationError("ID field must not be included in the registration request.")

        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError("Passwords do not match.")
        print('**************************************************************************************')
        print(data)
        print(type(data))
        print('**************************************************************************************')
        return data

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"]
        )
        return user










class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    total_amount = serializers.FloatField(read_only=True)
    # user= UserRegistrationSerializer()
    class Meta:
        model = Order
        fields = ["id", "user", "products", "total_amount", "created_at"]
        read_only_fields = ["total_amount", "created_at"]
        # depth=1

    def validate(self, data):
        total_amount = 0
        for product in data["products"]:
            if product.stock <= 0:
                raise serializers.ValidationError(f"Product {product.name} is out of stock.")
            total_amount += product.price
        data["total_amount"] = total_amount
        return data

    def create(self, validated_data):
        products = validated_data.pop("products")
        order = Order.objects.create(**validated_data)
        order.products.set(products)
        
        # Deduct stock
        for product in products:
            product.stock -= 1
            product.save()
        return order
