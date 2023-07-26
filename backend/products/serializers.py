from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Product
from .validator import validate_title,unique_title_validator
from api.serializers import UserPublicSerializer,UserProductInlineSerializer

class ProductSerializer(serializers.ModelSerializer):
    # nested Data (2 ways)
    # serializer
    owner= UserPublicSerializer(source='user',read_only=True)
    # inline
    related_product = UserProductInlineSerializer(source='user.product_set.all',read_only=True,many=True)

    
    my_discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='product-detail',
                                                lookup_field='pk')
    email = serializers.EmailField(write_only=True)
    title = serializers.CharField(validators=[validate_title,unique_title_validator])
    name = serializers.CharField(source='title',read_only=True)

    class Meta:
        model = Product
        fields=[
            'owner',
            'email',
            'url',
            'edit_url',
            'id',
            'title',
            'name',
            'content',
            'price',
            'sale_price',
            'my_discount',
            'related_product'
        ]

    def create(self,validated_data):
        # print(validated_data)
        # email = validated_data.pop('email')
        obj= super().create(validated_data)
        # return Product.objects.create(**validated_data)
        return obj
    
    def update(self,instance,validated_data):
        email = validated_data.pop('email')
        return super().update(instance,validated_data)

    def get_edit_url(self,obj):
        # return f"api/products/{obj.pk}"
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("product-edit",kwargs={"pk":obj.pk},request=request)

    def get_my_discount(self,obj):
        if not hasattr(obj,'id'):
            return None
        if not isinstance(obj,Product):
            return None
        try:
            return obj.get_discount()
        except:
            return None
            