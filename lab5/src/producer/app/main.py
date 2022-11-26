import time
import sys
import os
import argparse
from time import sleep
import pika
from contextlib import closing

parser = argparse.ArgumentParser()
parser.add_argument("--mq-host", help="RabbitMQ host", default="host.docker.internal")
parser.add_argument("--mq-port", help="RabbitMQ port", default="5672")
parser.add_argument("--mq-queue", help="RabbitMQ queue", default="hello")
args = parser.parse_args()

if __name__ == "__main__":
    with closing(pika.BlockingConnection(
            pika.ConnectionParameters(host=args.mq_host, port=args.mq_port, connection_attempts=10, retry_delay=5)
        )) as connection:
        with connection.channel() as channel:
            channel.queue_declare(queue=args.mq_queue)
            while True:
                try:
                    now = time.ctime()
                    channel.basic_publish(
                        exchange="", routing_key=args.mq_queue, body=f"Hello from {now}"
                    )
                    print(f" [x] Sent 'Hello World!' at {now}")
                    sleep(1)
                except KeyboardInterrupt:
                    print("Interrupted")
                    try:
                        sys.exit(0)
                    except SystemExit:
                        os._exit(0)
                except:
                    print("Waiting for something")
                    sleep(1)

# import pika

# while True:
#     try:
#         connection = pika.BlockingConnection(
#             pika.ConnectionParameters(host='host.docker.internal', port=5672,retry_delay=5, connection_attempts=10))
#         channel = connection.channel()

#         channel.queue_declare(queue='hello')

#         channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
#         print(" [x] Sent 'Hello World!'")
#         connection.close()
#         sleep(3)
#     except:
#         print("Retrying")
#         sleep(3)
