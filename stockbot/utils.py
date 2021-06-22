import threading
from time import sleep

from conf import RABBITMQ_HEARTBEAT_SLEEP_SECONDS
from services import ChatService

# Some helpers for main script


class WebsocketWrapper:
    socket = None


# webscoket_wrapper acts as a global variable that holds the websocket
# connection. This helps the consumer to send a message back to the client
websocket_wrapper = WebsocketWrapper()


def get_chat_websocket():
    """
    Returns the websocket connection saved in websocket_wrapper
    """
    return websocket_wrapper.socket


def sleep_and_retry_message(n=3):
    """
    Prints retry message for n seconds and sleeps for 1 second each time.
    """
    for i in range(n, 0, -1):
        print(f'Retrying in {i}')
        sleep(1)


def run_thread(callback, *args):
    """
    Instantiates a thread with a callback function, start it and return it.
    """
    t = threading.Thread(target=callback, args=args)
    t.start()
    return t


def send_heartbeat(channel, queue):
    """
    This avoids the "missed heartbeats" error of RabbitMQ
    """
    while True:
        channel.basic_publish(exchange='', routing_key=queue, body='')
        sleep(RABBITMQ_HEARTBEAT_SLEEP_SECONDS)


def get_chatroom_slug(auth_token):
    # Get list of chatrooms
    chat_service = ChatService(auth_token)
    chatrooms = chat_service.list_chatrooms()
    if chatrooms:
        print('Select chatroom: ')
        for i, chatroom in enumerate(chatrooms):
            print(f'{i+1}: {chatroom["topic"]}')
        n = input('Please enter the chatroom number to connect to: ')
        chatroom_count = len(chatrooms)
        while not n.isdigit() or int(n) not in range(chatroom_count):
            n = input('Not a valid option. Try again:')
        chosen_chatroom = chatrooms[int(n)-1]
        return chosen_chatroom['slug']
    else:
        print('No available chatrooms')