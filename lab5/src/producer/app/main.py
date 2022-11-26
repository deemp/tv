import time
import sys
import os
import argparse
from time import sleep
import pika
from contextlib import closing

parser = argparse.ArgumentParser()
parser.add_argument("--mq-host", help="RabbitMQ host")
parser.add_argument("--mq-port", help="RabbitMQ port")
parser.add_argument("--mq-queue", help="RabbitMQ queue")
args = parser.parse_args()

if __name__ == "__main__":
    with closing(
        pika.BlockingConnection(
            pika.ConnectionParameters(
                host=args.mq_host,
                port=args.mq_port,
                connection_attempts=10,
                retry_delay=5,
            )
        )
    ) as connection:
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