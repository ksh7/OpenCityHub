import pika, json, os, django
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_app.settings")
django.setup()

fake = Faker()

params = pika.URLParameters(os.getenv('RABBITMQ_HOST'))

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue=os.getenv('RABBITMQ_QUEUE'))

from control_panel.models import Event

def callback(ch, method, properties, body):
    print('Received in control_panel')
    print(json.loads(body))
    print(properties.content_type)
    event_name = fake.word()
    date = fake.date_between(start_date='today', end_date='+30d')
    location = fake.city()
    description = fake.paragraph()
    organizer_name = fake.name()

    event = Event.objects.create(
        event_name=event_name,
        date=date,
        location=location,
        description=description,
        organizer_name=organizer_name
    )
    event.save()

channel.basic_consume(queue=os.getenv('RABBITMQ_QUEUE'), on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()