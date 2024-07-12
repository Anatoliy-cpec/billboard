from django import forms
import os
from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Advertisement, Message, Author

image_extension = ['.jpg', '.png', '.bmp', '.gif', '.jpeg', '.svg', '.ico']

class PostForm(forms.ModelForm):
    class Meta:
       model = Advertisement
       fields = ['header', 'body', 'file_1', 'file_2', 'file_3', 'header_image', 'slots', 'author',
                  'category','status', 'response', 'accepted_authors', 'viewers', 'state',
                  'liked_authors', 'disliked_authors',]
       readonly_fields = ('status',)

class PostCreationForm(forms.ModelForm):
    class Meta:
       model = Advertisement
       fields = ['header', 'body', 'file_1', 'file_2', 'file_3', 'header_image', 'slots', 'category',]
       widgets = {'file_1': forms.FileInput,
                  'file_2': forms.FileInput,
                  'file_3': forms.FileInput,
                  'header_image': forms.FileInput,
                  }
    def clean(self):
            
            cleaned_data = super().clean()

            header = cleaned_data.get("header")
            if header is not None and len(header) > 40:
                raise ValidationError({
                    "header": f"The header cannot be more than 40 characters long. {len(header) - 40} char more than 40"
                })
            if len(header) < 6:
                 raise ValidationError({
                    "header": f"The header cannot be less than 6 characters long. {(len(header) - 6)*(-1)} char left"
                 })

            body = cleaned_data.get("body")
            if body is not None and len(body) < 20:
                 raise ValidationError({
                    "body": f"The body cannot be less than 20 characters long. {(len(body) - 20)*(-1)} char left"
                 })
            if len(body) > 100:
                 raise ValidationError({
                    "body": f"The body cannot be more than 200 characters long. {(len(body) - 200)} char more"
                 })
            
            if body == header:
                 raise ValidationError({
                    "body": ("The text and the title cannot be the same."),
                    "header": ("The text and the title cannot be the same."),
                 })
            
            slots = cleaned_data.get("slots")
            if slots is not None and slots < 1:
                 raise ValidationError({
                    "slots": f"The number of slots cannot be less than 1."
                 })
            if slots is not None and slots > 6:
                 raise ValidationError({
                    "slots": f"The number of slots cannot be more than 6."
                 })
            category = cleaned_data.get("category")
            if category is None:
                 raise ValidationError({
                    "category": "Please select a category."
                 })
            cover = cleaned_data.get("header_image")
            if cover is not None:
                  file = str(cover)
                  file_ext = os.path.splitext(file)[1]
                  if file_ext not in image_extension:
                        raise ValidationError({
                            "header_image": "Invalid image format. Please use JPG, PNG, GIF, BMP, JPEG, SVG or ICO."
                        })

            if cover is not None and cover.size > 5242880:
                 raise ValidationError({
                    "header_image": "Image size should not be more than 5MB."
                 })
            
            
            
            
            
            return cleaned_data  

class MessageForm(forms.ModelForm):
     class Meta:
          model = Message
          fields = ['message_text',]
          readonly_fields = ('author',)      
