from .models import Product
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

def validate_title(value):
    # qs = Product.objects.filter(title__iexact=value)
    if 'kaka' in value:
        raise serializers.ValidationError("title cannot contain kaka")
    return value


unique_title_validator = UniqueValidator(queryset=Product.objects.all(),lookup='iexact')