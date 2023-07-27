from rest_framework import generics
from products.models import Product
from products.serializers import ProductSerializer
from rest_framework.response import Response
from . import client


class SearchOldListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self,*args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get('q')
        results = Product.objects.none()
        if q is not None:
            user = None
            if self.request.user.is_authenticated:
                user = self.request.user
                results = qs.search(query=q,user=user)
        return results

class SearchListView(generics.GenericAPIView):
    def get(self,request,*args, **kwargs):
        query = request.GET.get('q')
        tags = request.GET.getlist('tag')
        user = None
        if request.user.is_authenticated:
            user = request.user.username
        if not query:
            return Response('',status=400)
        results = client.perform_search(query=query,tags=tags,user=user)
        return Response(results)

search_list_view = SearchListView.as_view()