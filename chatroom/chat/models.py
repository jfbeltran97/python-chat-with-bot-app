from autoslug import AutoSlugField

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class ChatRoom(models.Model):
    topic = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='topic', unique=True)
    # This was supposed to handle connected users
    # We could even have another ManyToManyField for banned users if we
    # want to add that functionality.
    users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.topic


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='messages')
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
