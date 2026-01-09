from django import forms
from .models import *

class modelform(forms.ModelForm):
    class Meta:
        model=product
        fields='__all__'