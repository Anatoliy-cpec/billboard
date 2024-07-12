from django.http import HttpRequest, HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404


from .filters import *

from .forms import ChatMessageCreateForm

from advertisement.models import Author
from .models import MyChat, ChatMessage

from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
)


class PersonalChatView(LoginRequiredMixin, FormMixin, DetailView):

    model = MyChat
    template_name = 'chat_personal.html'
    context_object_name = 'chat'
    queryset = MyChat.objects.get_queryset().order_by('id')
    form_class = ChatMessageCreateForm
    success_url = 'chat_personal/'
    

    def dispatch(self, request, *args, **kwargs):
        handler = super().dispatch(request, *args, **kwargs)
        user = request.user
        chat = self.get_object()
        if not (user in chat.users.all() or user.is_superuser):
            raise PermissionDenied
        return handler

    def get_success_url(self) -> str:
        return reverse_lazy('chat', kwargs={'pk': self.get_object().id})
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
                
    def form_valid(self, form) -> HttpResponse:
        self.form = form.save(commit=False)
        self.form.user = self.request.user
        self.chat = self.get_object()
        self.form.save()
        self.chat.messages.add(self.form)
        self.chat.save()
        return super().form_valid(form)

class ChatListView(LoginRequiredMixin, ListView):
    model = MyChat
    template_name = 'chat_list.html'   
    context_object_name = 'chats'
    