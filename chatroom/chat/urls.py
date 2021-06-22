from django.urls import path

from . import consumers, views


urlpatterns = [
    path('chatrooms/', views.ChatRoomListView.as_view(), name="chatroom-list"),
    path('chatrooms/<slug:slug>/', views.ChatRoomDetailView.as_view(), name="chatroom-detail"),
    path('api/chatrooms/', views.ChatRoomListAPIView.as_view(), name='chatroom-list-api')
]

websocket_urlpatterns = [
    path('chatrooms/<slug:slug>/', consumers.ChatRoomConsumer.as_asgi()),
]
