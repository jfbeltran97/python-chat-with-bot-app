from rest_framework import generics

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import  ChatRoom
from .serializers import ChatRoomSerializer


class ChatRoomListView(LoginRequiredMixin, ListView):
    model = ChatRoom
    context_object_name = 'chatrooms'


class ChatRoomDetailView(LoginRequiredMixin, DetailView):
    model = ChatRoom
    context_object_name = 'chatroom'


class ChatRoomListAPIView(generics.ListAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer