from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
import random

type = ['1','2','3','4','5','6']


class ProductQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(public=True)
    
    def search(self,query,user=None):
        lookup = Q(title__icontains = query) | Q(content__icontains = query)
        qs =  self.is_public().filter(lookup)
        if user is not None:
            # user can see their private product
            qs2 = qs.filter(user = user).filter(lookup)
            qs = (qs | qs2).distinct()
        return qs

class ProductManager(models.Manager):

    def get_queryset(self,*args, **kwargs):
        return ProductQuerySet(self.model, using=self._db, *args, **kwargs)

    def search(self,query,user= None):
        return self.get_queryset().is_public().search(query,user)

class Product(models.Model):


    user = models.ForeignKey(User,default=1,null=True,on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True, null=True)
    price =models.DecimalField(max_digits=15,decimal_places=2,default=99.99)
    public = models.BooleanField(default=True)
    objects = ProductManager()
    
    @property
    def body(self):
        return self.content
    
    @property
    def path(self):
        return f'api/products/{self.pk}'

    def is_public(self):
        return self.public

    def tag(self):
        return random.choice(type)

    @property
    def sale_price(self):
        return "%.2f" %(float(self.price) * 0.8)
    
    def get_discount(self):
        return "122"