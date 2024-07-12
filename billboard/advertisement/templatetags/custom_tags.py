
from django import template
from django.urls import reverse
import os
from advertisement.models import Category, Advertisement


register = template.Library()



@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()


@register.simple_tag
def category_counter(category_id):
   count = Advertisement.objects.filter(category__id=category_id)
   return count.count()

@register.simple_tag
def navactive(request, urls):
    if request.path in ( reverse(url) for url in urls.split() ):
        return "active"
    return ""

@register.simple_tag
def file_define(file):
    video_extension = ['.mp4', '.mkv', '.avi', '.flv', '.vob', '.swf', '.mov', '.wmv', '.3gp']
    image_extension = ['.jpg', '.png', '.bmp', '.gif', '.jpeg', '.svg', '.ico']
    archive_extension = ['.zip', '.rar', '.tar.gz', '.gz', '.7z']
    document_extension = ['.txt', '.doc','.pdf']
    
    file = str(file)
    file_ext = os.path.splitext(file)[1] # file name or location with extension

    if file_ext in video_extension:
        return 'video'
    elif file_ext in image_extension:
        return 'image'
    elif file_ext in archive_extension:
        return 'archive'
    elif file_ext in document_extension:
        return 'document'
    
@register.simple_tag
def responded(advertisement, author):
    if advertisement:
        for i in advertisement.response.all():
            if i.author == author:
                return True
        return False

    else:
        return False
        
