from django.conf.urls import url, include
from rest_framework import routers
from bookd.views import *


from rest_framework import routers


router = routers.DefaultRouter()
router.register('post', BookAdvertiseView, basename='post')

urlpatterns = [
    url(r'^all', GetAllPosts.as_view(), name='all'),
    url(r'^user-posts/$', GetAllUserPosts.as_view(), name='user-posts'),
    url(r'^(?P<username>[0-9a-zA-Z]+)/posts/$', GetPublicUserPosts.as_view(), name='public-posts-review')
] + router.urls