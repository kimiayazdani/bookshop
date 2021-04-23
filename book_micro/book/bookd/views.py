from django.shortcuts import render
import logging
from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django_plus.api import UrlParam as _p
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from bookd.models import BookAd
from bookd.serializers import (
    BookAdSerializer,
    BookAdUpdateSerializer,
    BookAdListSerializer,
    BookAdSerializerPost,
)


class BookAdvertiseView(ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    list_params_template = [
        _p('category', _p.list(separator=',', item_cleaner=_p.string)),
        _p('min_price', _p.int),
        _p('max_price', _p.int),
        _p('author', _p.string),
        _p('title', _p.string)
    ]

    def get_serializer_class(self):
        if self.request.method == 'GET' and self.action == 'list':
            return BookAdListSerializer
        elif self.request.method == 'PATCH':
            return BookAdUpdateSerializer
        elif self.request.method == 'POST':
            return BookAdSerializerPost
        return BookAdSerializer

    def get_serializer_context(self):
        if self.request.method == 'GET' and self.action == 'list':
            context = {
                'data': self.get_data(),
                'view': self,
            }
        return context

    def get_data(self):
        data = self.get_queryset()
        data = {d['id']: d for d in data}
        return data

    def get_queryset(self):
        _query = None
        if self.request.method == 'GET' and self.action == 'list':
            _query = BookAd.objects.filter(
                min_price=5
            )
            params = _p.clean_data(self.request.query_params, self.list_params_template)

            category = params['category']
            min_price = params['min_price']
            max_price = params['max_price']
            author = params['author']
            title = params['title']
            validation_kinds = self.validate_kinds(ad_types)
            if start > end:
                raise ValidationError('start datetime should be before end datetime')
            if not validation_kinds:
                raise ValidationError('kind should be in cat, dog or hamster ')

            if category:
                _query = _query.filter(kind__in=category)
            if max_price:
                _query = _query.filter(price__lte=max_price)
            if min_price:
                _query = _query.filter(price__gte=min_price)
            if title:
                _query = _query.filter(title__icontains=title)
            if author:
                _query = _query.filter(authorName__icontains=author)
            _query = _query.values(
                'id', 'category', 'title', 'price', 'author'
            )
        elif self.request.method == 'PATCH':
            _query = BookAd.objects.all()

        return _query

    @staticmethod
    def validate_kinds(kinds):
        return True

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs['pk']
        try:
            book_ad = BookAd.objects.get(id=pk)
        except BookAd.DoesNotExist:
            return Response(data={'object with id:{} does not exist'.format(pk)}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookAdSerializer(book_ad)
        data = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            post = BookAd.objects.get(id=pk)
        except BookAd.DoesNotExist:
            return Response(data={'object with id:{} does not exist'.format(pk)}, status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(post)
        return Response(data={'object deleted successfully'}, status=status.HTTP_200_OK)


class GetAllUserPosts(ListAPIView):
    serializer_class = AdAll

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance = None  # type: Optional[BookAd]

    def get_queryset(self):
        return BookAd.objects.filter(min_price=0)


class GetPublicUserPosts(ListAPIView):
    authentication_classes = ()
    serializer_class = AdAll

    def get_queryset(self):
        return BookAd.objects.filter(min_price=0)
