
from django.http import HttpRequest, HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.db import models


from .filters import AdvertisementSearchFilter

from .forms import PostForm, MessageForm, PostCreationForm

from .models import Advertisement, Category, Author, Message
from chat.models import MyChat

from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView, View
)



class AdvertisementList(ListView):
    model = Advertisement
    ordering = '-creation_date'
    template_name = 'advertisements.html'
    context_object_name = 'advertisements'
    paginate_by = 9

    
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AdvertisementSearchFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categorys = Category.objects.get_queryset().order_by('id')
        authors = Author.objects.get_queryset().order_by('id')
        
        context['categorys'] = categorys
        context['authors'] = authors.order_by('-rating')
        context['filterset'] = self.filterset
        return context
    
class MyAdvertisementList(LoginRequiredMixin, ListView):
    model = Advertisement
    ordering = '-creation_date'
    template_name = 'advertisements.html'
    context_object_name = 'advertisements'
    paginate_by = 9
    
    
    def get_queryset(self, **kwargs):
        
        author = self.request.user.author
        queryset = super().get_queryset(**kwargs).filter(author=author)
        self.filterset = AdvertisementSearchFilter(self.request.GET, queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categorys = Category.objects.get_queryset().order_by('id')
        authors = Author.objects.get_queryset().order_by('id')
        
        context['categorys'] = categorys
        context['authors'] = authors.order_by('-rating')
        context['filterset'] = self.filterset
        return context
    
    

    
class AdvertisementDetail(LoginRequiredMixin, FormMixin, DetailView):
    model = Advertisement
    template_name = 'advertisement.html'
    context_object_name = 'advertisement'
    queryset = Advertisement.objects.get_queryset().order_by('id')
    form_class = MessageForm
    success_url = 'advertisements/'

    def get_success_url(self) -> str:
        return reverse_lazy('advertisement', kwargs={'pk': self.get_object().id})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def get(self, request: HttpRequest, *args: reverse_lazy, **kwargs: reverse_lazy) -> HttpResponse:
        if not request.user.is_anonymous:
            self.advertisement = self.get_object()
            self.advertisement.views_conuter_add(request.user.author)

        return super().get(request, *args, **kwargs)
        
    def form_valid(self, form) -> HttpResponse:
        self.form = form.save(commit=False)
        self.form.author = self.request.user.author
        self.advertisement = self.get_object()
        self.form.save()
        self.advertisement.response.add(self.form)
        self.advertisement.save()
        return super().form_valid(form)

    
    
class AdvertisementResponses(LoginRequiredMixin, DetailView):
    model = Advertisement
    template_name = 'advertisement_responses.html'
    context_object_name = 'advertisement'
    queryset = Advertisement.objects.get_queryset().order_by('id')
    success_url = 'responses/'


    def dispatch(self, request, *args, **kwargs):
        handler = super().dispatch(request, *args, **kwargs)
        user = request.user
        advertisement = self.get_object()
        if not (advertisement.author.user == user or user.is_superuser):
            raise PermissionDenied
        return handler

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AdvertisementSearchFilter(self.request.GET, queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
    
    # def get_object(self, queryset=None):
    #     return get_object_or_404(Advertisement, pk=self.kwargs.get('pk'))



def  accept_response(self, pk, response_pk):
    advertisement = Advertisement.objects.get(pk=pk)
    response = Message.objects.get(pk=response_pk)
    advertisement.delete_response(response_pk)
    advertisement.add_author(response.author)
    return redirect(f'http://127.0.0.1:8000/advertisements/{pk}/responses/')

def  decline_response(self, pk, response_pk):
    advertisement = Advertisement.objects.get(pk=pk)
    advertisement.delete_response(response_pk)
    return redirect(f'http://127.0.0.1:8000/advertisements/{pk}/responses/')

def  remove_accepted_author(self, pk, author_id):
    advertisement = Advertisement.objects.get(pk=pk)
    author = Author.objects.get(pk=author_id)
    advertisement.remove_author(author)
    return redirect(f'http://127.0.0.1:8000/advertisements/{pk}')

def  like_author(self, pk, author_id):
    advertisement = Advertisement.objects.get(pk=pk)
    author = Author.objects.get(pk=author_id)
    advertisement, author
    
    if author in advertisement.disliked_authors.all():
        advertisement.disliked_authors.remove(author)
        advertisement.liked_authors.add(author)
        advertisement.save()
    if author in advertisement.liked_authors.all():
        pass
    else:
        advertisement.liked_authors.add(author)
        advertisement.save()

    return redirect(f'http://127.0.0.1:8000/advertisements/{pk}')

def  dislike_author(self, pk, author_id):
    advertisement = Advertisement.objects.get(pk=pk)
    author = Author.objects.get(pk=author_id)
    
    if author in advertisement.liked_authors.all():
        advertisement.liked_authors.remove(author)
        advertisement.disliked_authors.add(author)
        advertisement.save()
    if author in advertisement.disliked_authors.all():
        pass
    else:
        advertisement.disliked_authors.add(author)
        advertisement.save()

    return redirect(f'http://127.0.0.1:8000/advertisements/{pk}')

def state_change(self, pk):
    advertisement = Advertisement.objects.get(pk=pk)
       
    if advertisement.state == Advertisement.AdvertisementState.in_progress and not advertisement.status:
        advertisement.state = Advertisement.AdvertisementState.unfinished
        # Этот код не должен находиться здесь \\ПЕРЕНЕСТИ//
        users = advertisement.get_all_advertisement_users()
        __chat_id = MyChat.create_chat(new_users=users, name=advertisement.header, post_id=advertisement.id)
        advertisement.chat_id = __chat_id
        advertisement.save()
        

    elif advertisement.state == Advertisement.AdvertisementState.unfinished and advertisement.is_all_liked:
        advertisement.state = Advertisement.AdvertisementState.finished
        advertisement.rating_confirmation()
        # Этот код не должен находиться здесь \\ПЕРЕНЕСТИ//
        MyChat.objects.get(id=advertisement.chat_id).delete_chat()
        advertisement.save()


    return redirect(f'http://127.0.0.1:8000/advertisements/{pk}')




class AdvertisementCreate(  LoginRequiredMixin,
                            CreateView):
    form_class = PostCreationForm
    model = Advertisement
    template_name = 'Advertisement_create.html'
    success_url = 'http://127.0.0.1:8000/advertisements/'
    

    def form_valid(self, form):
        request  = self.request
        advertisement = form.save(commit=False)
        advertisement.author = request.user.author
        return super().form_valid(form)

class AdvertisementUpdate(  LoginRequiredMixin,
                            UpdateView):
    form_class = PostCreationForm
    model = Advertisement
    context_object_name = 'advertisement'
    queryset = Advertisement.objects.get_queryset().order_by('id')
    template_name = 'Advertisement_create.html'
    success_url = 'http://127.0.0.1:8000/advertisements/'

    def dispatch(self, request, *args, **kwargs):
        handler = super().dispatch(request, *args, **kwargs)
        user = request.user
        advertisement = self.get_object()
        if not (advertisement.author.user == user or user.is_superuser):
            raise PermissionDenied
        return handler

