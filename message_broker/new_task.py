#!/usr/bin/env python3
import pika
import sys

queues = ["bf", "dict", "gpu"]

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

message = ' '.join(sys.argv[1:])

# send hash to all worker queues
for q in queues:
	channel.queue_declare(queue=q, durable=True)

	channel.basic_publish(exchange='',
	                      routing_key=q,
	                      body=message,
	                      properties=pika.BasicProperties(
	                         delivery_mode = 2, # make message persistent
                      ))
	print(" [x] Sent {} to queue {}".format(message, q))

connection.close()