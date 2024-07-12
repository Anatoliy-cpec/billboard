

from django.http import HttpRequest, HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from .forms import AuthorEditForm

from advertisement.models import Author

from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView,
)


class ProfileDetail(LoginRequiredMixin, DetailView):
    model = Author
    template_name = 'author_profile.html'
    context_object_name = 'author'
    queryset = Author.objects.all()

class ProfileAuthorEdit(LoginRequiredMixin, UpdateView):
    model = Author
    template_name = 'author_profile_edit.html'
    context_object_name = 'author'
    queryset = Author.objects.all()
    form_class = AuthorEditForm

    def get_success_url(self) -> str:

        return reverse_lazy('profile', kwargs={'pk': self.object.pk})
        



