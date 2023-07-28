from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Product

@register(Product)
class ProductIndex(AlgoliaIndex):
    fields = ('title', 'content','price','user','sale_price','public')
    settings = {'searchableAttributes': ['title'], 'attributesForFaceting': ['public','user']}
    tags = 'tag'