from django.db.models import fields
from product.models import *
from django import forms

class ImageForm(forms.ModelForm):
    class Meta:
        model=ProductImage
        fields=['file_path']