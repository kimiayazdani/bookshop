
import os
from collections import OrderedDict

from django.conf import settings
from django.core.files import File
from django.db import transaction
from rest_framework import serializers


from bookd.models import BookAd





class BookAdSerializerPost(serializers.ModelSerializer):
    
    class Meta:
        model = BookAd
        fields = [
            'id', 'category', 'title', 'author',
             'price', 'author'
        ]
        read_only_fields = ('id',)

    def get_user_id(self):
        return self.context['user_id']

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        return BookAd.objects.create(
            **validated_data
        )


class BookAdSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BookAd
        fields = [
            'id', 'title', 'author', 'price', 'author', 'category'
        ]
        read_only_fields = ('id',)



class BookAdUpdateSerializer(serializers.ModelSerializer):
    """
        this serializer used for PATCH request
    """
    poster = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = BookAd
        fields = (
            'id',
            'title',
            'price',
            'author',
            'category',
        )
        writable_fields = ('title', 'category', 'author', 'price')


    def update(self, instance: BookAd, validated_data):
        with transaction.atomic():
            for field in self.Meta.writable_fields:
                if field in validated_data:
                    setattr(instance, field, validated_data[field])
            instance.save()
            return super(BookAdUpdateSerializer, self).update(instance, validated_data)


class BookAdListSerializer(serializers.ModelSerializer):
    """
        this serializer used for GET request with action:list
    """
    

    class Meta:
        model = BookAd
        context_fields = (
            'id',
            'title',
            'category',
            'price',
            'author',
        )
        fields = context_fields
        read_only_fields = context_fields

    def to_representation(self, instance):
        
        
        ret = OrderedDict()
        fields = self.Meta.context_fields
        for field in fields:
            if field in self.Meta.fields:
                ret[field] = self.context['data'][instance['id']][field]
        return ret




