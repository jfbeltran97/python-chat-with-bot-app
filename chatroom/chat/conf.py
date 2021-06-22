from django.conf import settings


CHAT_MESSAGE_COUNT = getattr(settings, 'CHAT_MESSAGE_COUNT', 50)