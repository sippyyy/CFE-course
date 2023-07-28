from algoliasearch_django import raw_search
from products.models import Product

def perform_search(query,*args,**kwargs):
    tag_param = kwargs.get('tags')
    user_auth = kwargs.get('user')
    facetFilters=[['public:True', f'user:{user_auth}']]
    params = {'tagFilters': tag_param,'facetFilters':facetFilters}
    response = raw_search(Product, query,params)
    return response