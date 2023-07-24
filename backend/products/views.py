from django.shortcuts import get_object_or_404

# Create your views here.
from rest_framework import generics,mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from.serializers import ProductSerializer

from api.mixins import StaffEditorPermissionMixin


class ProductListCreateApiView(StaffEditorPermissionMixin,
                               generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def perform_create(self, serializer):
        # serializer.save(owner=self.request.user)
        title = serializer.validated_data['title']
        content = serializer.validated_data['content']
        if content is None:
            content = title
        serializer.save(content=content)


product_list_create_view = ProductListCreateApiView.as_view()

class ProductDetailView(StaffEditorPermissionMixin,
                        generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

product_detail_view = ProductDetailView.as_view()


class ProductUpdateView(StaffEditorPermissionMixin,
                        generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    

    def perform_update(self,serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title

product_update_view = ProductUpdateView.as_view()


class ProductDeleteView(StaffEditorPermissionMixin,
                        generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_destroy(self,instance):
        super().perform_destroy(instance)

product_delete_view = ProductDeleteView.as_view()

# class ProductListAPIView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

# product_list_view = ProductListAPIView.as_view()


class ProductMixinView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        generics.GenericAPIView,):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self,request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
    def post(self,request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    def perform_create(self, serializer):
        # serializer.save(owner=self.request.user)
        title = serializer.validated_data['title']
        content = serializer.validated_data['content']
        if content is None:
            content = title
        serializer.save(content=content)

product_mixin_view = ProductMixinView.as_view()




@api_view(['GET','POST'])
def product_alt_view(request,pk=None):
    method = request.method
    if method == "GET":
        if pk is not None:
            # querysetByPk = Product.objects.filter(pk=pk).first()
            # if not querysetByPk.exist():
            #     raise Http404
            # Do the same by rest django api
            obj = get_object_or_404(Product,pk=pk)
            data = ProductSerializer(obj,many=False).data
            return Response(data)
            
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset,many=True).data
        return Response(serializer)

    if method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data['title']
            content = serializer.validated_data['content'] or None
            if content is None:
                content = title
            serializer.save(content=content)
            print(serializer.data)
            return Response(serializer.data)
        return Response({"invalid":"invalid data"},status = 400)
