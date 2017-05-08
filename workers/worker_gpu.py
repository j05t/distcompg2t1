#!/usr/bin/env python3
import pika
import subprocess

hc = "hashcat/hashcat64.bin"

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='gpu', durable=True)


def callback(ch, method, properties, body):
    hash = body.decode("utf-8")
    print ("[x] Received ", hash)
    ch.basic_ack(delivery_tag = method.delivery_tag)

    # write hash to temporary file
    f = open("/tmp/crackme", "w+")
    f.write(hash)
    f.close()

    # find collision using gpu bruteforce, todo: set timeout
    r = subprocess.run([hc, "-a3", "/tmp/crackme"])

    if r.returncode == 0:
      msg = subprocess.run([hc, "--show", "/tmp/crackme"], stdout=subprocess.PIPE)
      msg = msg.stdout.decode("utf-8")
      # publish result
      print("[x] Done, publishing to result queue")
      channel.queue_declare(queue="result", durable=True)
      channel.basic_publish(exchange='',
                            routing_key=hash,
                            body="cracked with gpu bruteforce:" + msg,
                            properties=pika.BasicProperties(
                               delivery_mode = 2, # make message persistent
                            ))

channel.basic_consume(callback, queue='gpu')

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()