from django.forms.models import model_to_dict
from products.models import Product
from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.serializers import ProductSerializer


@api_view(["POST"])
def api_home(request,*args,**kwargs):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():

        print(serializer.data)
        serializer.save()
        data = serializer.data 
        return Response(data)
    
    return Response({"message":"invalid"})
