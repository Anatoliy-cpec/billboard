from django import forms
import os
from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import MyChat, ChatMessage

class MyChatForm(forms.ModelForm):
     class Meta:
            model = MyChat
            fields = ['users', 'messages',]
            
class ChatMessageCreateForm(forms.ModelForm):
        class Meta:
            model = ChatMessage
            fields = ['message',]

        def clean(self):

            cleaned_data = super().clean()

            message = cleaned_data.get("message")
            if message is None:
                raise ValidationError({
                    "message": f"Сообщение не может быть пустым"
                })
            if len(message) > 300:
                 raise ValidationError({
                    "message": f"Сообщение не может быть длинне 300 символов. На {(len(message) - 300)} символа больше"
                 })
            
            return cleaned_data 
