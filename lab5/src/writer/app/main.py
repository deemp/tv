import argparse
import pika


# parser = argparse.ArgumentParser(
#     prog="writer",
#     description="Writes messages to RabbitMQ"
# )

# parser.add_argument("-h", "--host", default=)  # option that takes a value
# parser.add_argument("-p", "--port")

if __name__ == "__main__":
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="host.docker.internal", ))
    channel = connection.channel()

    channel.queue_declare(queue="hello")

    channel.basic_publish(exchange="", routing_key="hello", body="Hello World!")
    print(" [x] Sent 'Hello World!'")
    connection.close()
