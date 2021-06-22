import pika

# This should be an untracked file for git but in this case it is left
# this way because of simplicity

RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5678
RABBITMQ_HEARTBEAT_SLEEP_SECONDS = 10
QUEUE_NAME = 'stockbot'

BOT_USERNAME = 'stockbot'
BOT_PASSWORD = '12345'

SERVER_SCHEMA = 'http'
SERVER_HOST = 'localhost:8000'
SERVER_API_LOGIN_ENDPOINT = '/api/login/'
SERVER_API_CHATROOM_LIST_ENDPOINT = '/api/chatrooms/'

WS_SCHEMA = 'ws'
WS_HOST = 'localhost:8000'
WS_CHATROOM_PREFIX = '/chatrooms'


DEFAULT_CONNECTION_PARAMETERS = pika.ConnectionParameters(
    host=RABBITMQ_HOST,
    port=RABBITMQ_PORT,
)