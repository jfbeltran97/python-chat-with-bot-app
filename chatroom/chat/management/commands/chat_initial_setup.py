from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from chat.models import ChatRoom


User = get_user_model()


class Command(BaseCommand):
    help = 'Initial chat setup for testing purposes'

    def handle(self, *args, **options):
        User.objects.create_user(username="testUser", password="12345")
        User.objects.create_user(username="otherUser", password="12345")
        User.objects.create_user(username="stockbot", password="12345")

        ChatRoom.objects.create(topic="Test ChatRoom")

        print("User 1 created\nUsername:testUser\nPassword:12345\n")
        print("User 2 created\nUsername:otherUser\nPassword:12345\n")

    
