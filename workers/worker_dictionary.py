#!/usr/bin/env python3
import pika
import subprocess

hc = "hashcat/hashcat64.bin"

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='dict', durable=True)


def callback(ch, method, properties, body):
    hash = body.decode("utf-8")
    print ("[x] Received ", hash)
    ch.basic_ack(delivery_tag = method.delivery_tag)

    # write hash to temporary file
    f = open("/tmp/crackme_dict", "w+")
    f.write(hash)
    f.close()

    # find collision using gpu dictionary attack, todo: set timeout
    r = subprocess.run([hc, "-w3", "/tmp/crackme_dict", "hashcat/example.dict"])

    if r.returncode == 0:
      msg = subprocess.run([hc, "--show", "/tmp/crackme_dict"], stdout=subprocess.PIPE)
      msg = msg.stdout.decode("utf-8").strip('\n')
      # publish result
      print("[x] Done, publishing to result queue")
      channel.queue_declare(queue="result", durable=True)
      channel.basic_publish(exchange='',
                            routing_key=hash,
                            body="cracked with gpu dictionary attack:" + msg,
                            properties=pika.BasicProperties(
                               delivery_mode = 2, # make message persistent
                            ))

channel.basic_consume(callback, queue='dict')

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()