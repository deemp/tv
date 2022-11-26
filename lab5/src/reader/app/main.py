import sys
import os
import pika
import time
from time import sleep


def main():

    channel = None
    ok = False
    while not ok:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host="host.docker.internal", port="5672")
            )
            channel = connection.channel()
            channel.queue_declare(queue="hello")
            ok = True
        except Exception:
            print("Waiting for broker")
            sleep(2)

    try:

        def callback(ch, method, properties, body):
            print(f" [x] Received {body} at {time.ctime()}")

        channel.basic_consume(
            queue="hello", on_message_callback=callback, auto_ack=True
        )
        print(" [*] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()
    except KeyboardInterrupt as exc:
        raise KeyboardInterrupt from exc
    except Exception:
        print("Broker disconnected!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted!")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
