from algoliasearch_django import raw_search
from products.models import Product

def perform_search(query,*args,**kwargs):
    tag_param = kwargs.get('tags')
    user_auth = kwargs.get('user')
    facetFilters=[['public:true', 'user:thuy']]
    params = { "hitsPerPage": 5 ,'tagFilters': tag_param,'facetFilters':facetFilters}
    response = raw_search(Product, query,params)
    return response
