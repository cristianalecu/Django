from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core import serializers

from celery import shared_task

@shared_task #(queue="orders")
def create_order(order):
    return serializers.serialize('json',[order])