from django.urls import path
from .api import get_conf


urlpatterns = [
    path('get_config', get_conf, name='get_conf'),
]