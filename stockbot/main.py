import asyncio
import json

import pika
from websockets import connect
from websockets.exceptions import ConnectionClosedError

from services import AuthService, ChatService, build_url
from bot import StockBot
from conf import (
    DEFAULT_CONNECTION_PARAMETERS,
    QUEUE_NAME,
    WS_SCHEMA,
    WS_HOST,
    WS_CHATROOM_PREFIX,
)
from consumer import start_consumer
from utils import (
    websocket_wrapper,
    run_thread,
    sleep_and_retry_message,
    send_heartbeat,
    get_chatroom_slug
)


# Bot is just another user (should be created in server)
# Check conf.py for credentials
auth_service  = AuthService()
auth_service.login()

# Initialize bot instance
bot = StockBot()


async def listen_for_new_message(websocket):
    """
    Main loop. Await a message from socket and process it.
    """
    while True:
        msg = await websocket.recv()
        msg = json.loads(msg)
        if msg.get('is_new'):
            response = bot.process_message(msg['content'])
            if response:
                channel.basic_publish(
                    exchange='',
                    routing_key=QUEUE_NAME,
                    body=response
                )


async def stockbot(url):
    """
    Try to establish a connection with the server. If failed, try again 
    a few seconds later.
    """
    while True:
        try:
            async with connect(
                url, extra_headers=auth_service.headers
            ) as websocket:
                print('Connected!!')
                websocket_wrapper.socket = websocket
                await listen_for_new_message(websocket)
        except ConnectionRefusedError:
            print('Failed to connect to websocket. Server may be down.')
            sleep_and_retry_message()
        except ConnectionClosedError:
            print('Connection closed unexpectedly.')
            sleep_and_retry_message()


# Let user choose the chatroom
chatroom_slug = get_chatroom_slug(auth_service.token)
if chatroom_slug:
    chatroom_endpoint = f'{WS_CHATROOM_PREFIX}/{chatroom_slug}/'
    chatroom_url = build_url(host=WS_HOST, schema=WS_SCHEMA, endpoint=chatroom_endpoint)


    # Establish pika connection with RabbitMQ
    connection = pika.BlockingConnection(DEFAULT_CONNECTION_PARAMETERS)
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)

    # Must start consumer from this script otherwise it is not possible
    # (or really difficult) to share variables
    consumer_thread = run_thread(start_consumer)
    heartbeat_thread = run_thread(send_heartbeat, channel, QUEUE_NAME)

    asyncio.run(stockbot(chatroom_url))

    connection.close()
    print('Closed connection.')