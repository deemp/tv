import sys
import os
import time
from contextlib import closing
from time import sleep
import argparse
import psycopg2
import pika


parser = argparse.ArgumentParser()
parser.add_argument("--mq-host", help="RabbitMQ host", default="host.docker.internal")
parser.add_argument("--mq-port", help="RabbitMQ port", default="5672")
parser.add_argument("--mq-queue", help="RabbitMQ queue", default="hello")
parser.add_argument("--db-name", help="PostgreSQL database name", default="db_postgres")
parser.add_argument("--db-user", help="PostgreSQL database user", default="root")
parser.add_argument("--db-pass", help="PostgreSQL database password", default="root")
args = parser.parse_args()

def main():
    # with closing(psycopg2.connect(dbname=args.db_name, user=args.db_user, password = args.db_pass)) as conn:
    #     with conn.cursor() as cursor:
            with pika.BlockingConnection(
                pika.ConnectionParameters(host=args.mq_host, port=args.mq_port, connection_attempts=10, retry_delay=5)
            ) as pika_conn:
                with pika_conn.channel() as channel:
                    def callback(ch, method, properties, body):
                        print(f" [x] Received {body} at {time.ctime()}")
                        # try:
                        #     cursor.execute(f'SELECT * FROM {args.db_name}')
                        #     print("Selected from db")
                        #     for row in cursor:
                        #             print(row)
                        # except Exception as exc:
                        #     print("DB exception!")
                        #     raise exc
                    for j in range(5):
                        print(f"Attempt {j}. Reading from MQ")
                        try:
                            channel.queue_declare(queue=args.mq_queue)
                            channel.basic_consume(
                                queue=args.mq_queue, on_message_callback=callback, auto_ack=True
                            )
                            print(" [*] Waiting for messages. To exit press CTRL+C")
                            channel.start_consuming()
                        except KeyboardInterrupt:
                            print("Interrupted!")
                            try:
                                sys.exit(0)
                            except SystemExit:
                                os._exit(0)
                        except Exception:
                            print("Some exception occured! Retrying")
                            sleep(1)


if __name__ == "__main__":
    main()
            
            
# import sys
# import os
# import pika
# import time
# from time import sleep
# import psycopg2


# def main():

#     channel = None
#     ok = False
#     while not ok:
#         try:
#             connection = pika.BlockingConnection(
#                 pika.ConnectionParameters(host="host.docker.internal", port="5672")
#             )
#             channel = connection.channel()
#             channel.queue_declare(queue="hello")
#             ok = True
#         except Exception:
#             print("Waiting for broker")
#             sleep(2)

#     try:

#         def callback(ch, method, properties, body):
#             print(f" [x] Received {body} at {time.ctime()}")

#         channel.basic_consume(
#             queue="hello", on_message_callback=callback, auto_ack=True
#         )
#         print(" [*] Waiting for messages. To exit press CTRL+C")
#         channel.start_consuming()
#     except KeyboardInterrupt as exc:
#         raise KeyboardInterrupt from exc
#     except Exception:
#         print("Broker disconnected!")


# if __name__ == "__main__":
#     try:
#         main()
#     except KeyboardInterrupt:
#         print("Interrupted!")
#         try:
#             sys.exit(0)
#         except SystemExit:
#             os._exit(0)
