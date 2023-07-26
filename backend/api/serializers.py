from rest_framework import serializers


class UserProductInlineSerializer(serializers.Serializer):
    title = serializers.CharField(read_only=True)
    url = serializers.HyperlinkedIdentityField(read_only=True, view_name='product-detail',lookup_field='pk')

class UserPublicSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    id = serializers.CharField(read_only=True)
    other_products = serializers.SerializerMethodField(read_only=True)

    def get_other_products(self,obj):
        products = obj.product_set.all()
        return UserProductInlineSerializer(products,many=True,context=self.context).data