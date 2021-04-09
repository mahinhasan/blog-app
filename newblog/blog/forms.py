from django import forms
from django.forms import fields, widgets
from ckeditor.widgets import CKEditorWidget

from .models import Article,Author


class ArticleForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Article
        fields = ['title','text','image','category']

        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'text':forms.Textarea(attrs={})
            
        }

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['detail','profile_pic']