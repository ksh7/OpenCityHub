import os
import pika, json

params = pika.URLParameters(os.getenv('RABBITMQ_HOST'))
connection = pika.BlockingConnection(params)
channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key=os.getenv('RABBITMQ_QUEUE'), body=json.dumps(body), properties=properties)