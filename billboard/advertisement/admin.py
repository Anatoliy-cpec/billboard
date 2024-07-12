from django.contrib import admin
from .forms import PostForm
from .models import Advertisement, Author, Category, Message

# Register your models here.
@admin.register(Advertisement)
class PostAdmin(admin.ModelAdmin):
    form = PostForm



register = admin.site.register(Author)
register = admin.site.register(Message)
register = admin.site.register(Category)