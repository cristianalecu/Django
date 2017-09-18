import pika

from django.core import serializers
from constance import config

def create_order2(order):
	try:
		print(config.RABBITMQ_BROKER_URL)
		connection = pika.BlockingConnection(pika.URLParameters(config.RABBITMQ_BROKER_URL))
		channel = connection.channel()
		channel.queue_declare(queue=config.RABBITMQ_ORDERS_QUEUE)
		channel.basic_publish(exchange='', routing_key=config.RABBITMQ_ORDERS_QUEUE, body=serializers.serialize('json',[order]))
		connection.close()
	except Exception as e:
		print(e)