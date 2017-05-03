#!/usr/bin/env python3
import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='gpu', durable=True)


def callback(ch, method, properties, body):
    print ("[x] Received {}".format(body))
    ch.basic_ack(delivery_tag = method.delivery_tag)
    # simulate cpu intensive task
    time.sleep( 1)
    print("[x] Done")

channel.basic_consume(callback, queue='gpu')

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()