from django import forms
import os
from advertisement.models import Author
from django.core.exceptions import ValidationError

image_extension = ['.jpg', '.png', '.bmp', '.gif', '.jpeg', '.svg', '.ico']

class AuthorEditForm(forms.ModelForm):
    class Meta:
          model = Author
          fields = ['profile_photo','bio','first_name',]
          widgets = {'profile_photo': forms.FileInput,
                     
                     }

    def clean(self):
                    cleaned_data = super().clean()
                    cover = cleaned_data.get("profile_photo")
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
                    name = cleaned_data.get("first_name")
                    if name and len(name) > 15:
                            raise ValidationError({
                                    "first_name": "Name should not be more than 15 characters long."
                            })
                    bio = cleaned_data.get("bio")
                    if bio and len(bio) > 400:
                            raise ValidationError({
                                    "bio": "Bio should not be more than 200 characters long."
                            })
        
                    return cleaned_data