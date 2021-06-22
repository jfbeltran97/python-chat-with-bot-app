import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from django.utils import timezone

from .conf import CHAT_MESSAGE_COUNT
from .models import ChatRoom, ChatMessage


class ChatRoomConsumer(WebsocketConsumer):
    chat_message_type = 'chat.message'
    chat_connection_type = 'chat.connection'
    chat_disconnection_type = 'chat.disconnection'

    def connect(self):
        """
        Add a client to a broadcast group and accept the connection
        """
        chatroom_slug = self.scope['url_route']['kwargs']['slug']
        self.chatroom = ChatRoom.objects.get(slug=chatroom_slug)
        self.room_group_name = f'chat_{chatroom_slug}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        # Send last messages
        messages = self.chatroom.messages.select_related('user')[:CHAT_MESSAGE_COUNT:-1]
        for message in messages:
            self.send(json.dumps({
                'created_at': message.created_at,
                'user': message.user.username,
                'content': message.content,
                'type': self.chat_message_type,
            }, default=str))


        # Send new connection message
        self.user = self.scope['user']
        self.group_send({
            'user': self.user.username,
            'type': self.chat_connection_type
        })

    def receive(self, text_data=None, bytes_data=None):
        """
        Receive message from WebSocket and forward it to group
        """
        content = text_data or bytes_data.decode()
        message = ChatMessage.objects.create(
            user=self.user,
            chatroom=self.chatroom,
            content=content
        )
        message_data = {
            'created_at': message.created_at,
            'user': self.user.username,
            'content': content,
            'type': self.chat_message_type,
            'is_new': True, # for chatbot
        }

        self.group_send(message_data)
    
    def chat_message(self, event):
        """
        Receive message from group and forward it back to WebSocket
        """
        message = event['message']

        self.send(text_data=json.dumps(message, default=str))
    
    def group_send(self, message, message_type=chat_message_type):
        """
        Wraps async_to_sync for this consumer to avoid repetition
        """
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': message_type,
                'message': message
            }
        )

    def disconnect(self, code):
        self.group_send({
            'user': self.user.username,
            'type': self.chat_disconnection_type
        })
        self.close(code)
        