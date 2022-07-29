from collections import OrderedDict
from rest_framework import serializers
from .models import Receipt, User, Shop, Product


class PostProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    count = serializers.IntegerField()
    price = serializers.IntegerField()
    product_sum = serializers.IntegerField(required=False)
    
    class Meta:
        model = Product
        exclude = ['receipt']


class GetProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    receipt = serializers.PrimaryKeyRelatedField(queryset=Receipt.objects.all())
    count = serializers.IntegerField()
    price = serializers.IntegerField()
    product_sum = serializers.IntegerField()
    
    class Meta:
        model = Product
        fields = '__all__'
        

class PostReceiptSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    shop = serializers.CharField()
    product = PostProductSerializer(many=True)
    date_of_issue = serializers.DateTimeField()
    total_sum = serializers.IntegerField(required=False)
    
    class Meta:
        model = Receipt
        fields = ('id', 'user', 'check_number', 'product', 'shop', 'date_of_issue', 'total_sum')
        depth = 1
    
    def create(self, validated_data):
        """
        In create() we guarantee the correct calculation
        of the total sum and product sum or its calculation if it was not sent
        """
        products = validated_data.pop('product')
        if validated_data:
            if 'total_sum' not in validated_data.keys():
                print(products[0].keys())
                product_sum = [0 if 'product_sum' not in product.keys()
                               else product['product_sum'] for product in products]
                print(product_sum)
                receipt = Receipt.objects.create(total_sum=sum(product_sum), **validated_data)
                receipt.total_sum = 0
                for product in products:
                    product_map = OrderedDict((key, val) for key, val in product.items())
                    product = Product(receipt=receipt, **product_map)
                    product.save()
                    receipt.total_sum += product.product_sum
                receipt.save()

            else:
                receipt = Receipt.objects.create(**validated_data)
                products_total_sum = 0
                for product in products:
                    product_map = OrderedDict((key, val) for key, val in product.items())
                    product = Product(receipt=receipt, **product_map)
                    product.save()
                    products_total_sum += product.product_sum
                receipt.total_sum = products_total_sum
                receipt.save()
            return receipt


class GetReceiptSerializer(serializers.ModelSerializer):
    product = GetProductSerializer(many=True, read_only=True)

    class Meta:
        depth = 1
        model = Receipt
        fields = ('id', 'user', 'check_number', 'product', 'shop', 'date_of_issue', 'total_sum')
        
        
class UserShopsSerializer(serializers.Serializer):
    name = serializers.CharField()
    shops = serializers.DictField()
    
    class Meta:
        fields = ('name', 'shops')
        

class SumPerTimeSerializer(serializers.Serializer):
    date_from = serializers.DateTimeField()
    date_to = serializers.DateTimeField()
    total_sum = serializers.IntegerField()
    
    class Meta:
        fields = ('date_from', 'date_to', 'total_sum')


class ReceiptsPerTimeSerializer(serializers.Serializer):
    date_from = serializers.DateTimeField()
    date_to = serializers.DateTimeField()
    receipts = serializers.ListField()
    
    class Meta:
        fields = ('date_from', 'date_to', 'receipts')