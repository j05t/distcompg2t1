#!/usr/bin/env python3
import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='gpu', durable=True)


def callback(ch, method, properties, body):
    hash = body.decode("utf-8")
    print ("[x] Received ", hash)
    ch.basic_ack(delivery_tag = method.delivery_tag)

    # simulate cpu intensive task
    time.sleep( 1)

    # publish to queue result
    print("[x] Done, publishing to result queue")
    channel.queue_declare(queue='result', durable=True)
    channel.basic_publish(exchange='',
                          routing_key="result",
                          body="cracked with gpu bruteforce:" + hash,
                          properties=pika.BasicProperties(
                             delivery_mode = 2, # make message persistent
                          ))

channel.basic_consume(callback, queue='gpu')

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()