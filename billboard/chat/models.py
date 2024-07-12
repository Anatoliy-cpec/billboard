from django.db import models
from django.contrib.auth.models import User



class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    message = models.TextField(verbose_name='Сообщение', max_length=300)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')

    def __str__(self) -> str:
        return f"{self.user,'|', self.message}"


class MyChat(models.Model):
    chat_name = models.CharField(verbose_name='Чат для объявления:', max_length=32)
    advertisement_id = models.PositiveIntegerField(blank=True, null=True)
    users = models.ManyToManyField(User, related_name='users')
    messages = models.ManyToManyField(ChatMessage, verbose_name='Chat Message', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    @staticmethod
    def create_chat(new_users, name:str, post_id):
        chat = MyChat.objects.create()
        for user in new_users:
            chat.users.add(user)
        chat.chat_name = name
        chat.advertisement_id = post_id
        chat.save()
        return chat.id

    def delete_chat(self):
        self.messages.all().delete()
        self.users.clear()
        self.delete()
        

    def __str__(self) -> str:
        return f' Chat №  {self.id}'

    