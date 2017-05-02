#!/usr/bin/env python3
import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='dict', durable=True)


def callback(ch, method, properties, body):
    print ("[x] Received {}".format(body))
    time.sleep( 1)
    print("[x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_consume(callback, queue='dict')

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()