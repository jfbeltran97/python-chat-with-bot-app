import asyncio, sys
import pika
from asgiref.sync import async_to_sync

from conf import DEFAULT_CONNECTION_PARAMETERS, QUEUE_NAME
from utils import get_chat_websocket


def callback(ch, method, properties, body):
    websocket = get_chat_websocket()
    if websocket and body:
        # asyncio.run(websocket.send(body.decode()))
        async_to_sync(websocket.send)(body.decode())
        print(" [x] Received ", body)


def start_consumer():
    connection = pika.BlockingConnection(DEFAULT_CONNECTION_PARAMETERS)
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        start_consumer()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)