import time
import sys
import os
from time import sleep
import pika

if __name__ == "__main__":
    connection = None
    ok = False
    while not ok:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host="host.docker.internal", port=5672)
            )
            channel = connection.channel()
            channel.queue_declare(queue="hello")
            ok = True
        except Exception:
            print("Waiting for broker")
            time.sleep(1)
    while True:
        try:
            now = time.ctime()
            channel.basic_publish(
                exchange="", routing_key="hello", body=f"Hello from {now}"
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
