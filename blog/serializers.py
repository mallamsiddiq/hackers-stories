from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Items



class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ('__all__')
        # exclude=['api_id']