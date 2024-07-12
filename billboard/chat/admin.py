from django.contrib import admin
from . models import ChatMessage, MyChat

register = admin.site.register(ChatMessage)
register = admin.site.register(MyChat)