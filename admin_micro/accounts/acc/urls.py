from django.urls import path
from .views import *


urlpatterns = [
    path('check_if_account_exists/', does_account_exist_view, name="check_if_account_exists"),
    path('properties/', account_properties_view, name="properties"),
    path('update/', update_account_view, name="update"),
    path('login/', Login.as_view(), name="login"),

]
