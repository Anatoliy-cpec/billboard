from django.urls import path

from .views import (
    PersonalChatView, ChatListView,

)


urlpatterns = [
    path('', ChatListView.as_view(), name='chats'),
    path('<int:pk>', PersonalChatView.as_view(), name='chat'),

]