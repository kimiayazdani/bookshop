import base64
from django.core.exceptions import ValidationError

from django.contrib.auth.hashers import make_password
from django.core.files import File
from rest_framework import serializers
from django.db import transaction

from .models import Account






class AccountPropertiesSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ['pk', 'email', 'bio', 'phone_number', 'username', 'name']


class AccountUpdateSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False)

    class Meta:
        model = Account
        fields = ['pk', 'phone_number', 'bio', 'name', 'username', 'password']
        read_only_fields = ['pk']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def update(self, instance, validated_data):
        if validated_data.get('password', None):
            validated_data['password'] = make_password(validated_data['password'])
        return super(AccountUpdateSerializer, self).update(instance, validated_data)


