from django import forms
from django.forms import fields, widgets
from ckeditor.widgets import CKEditorWidget
from django.utils.translation import ugettext_lazy as _

from .models import Article,Author,Comment


class ArticleForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Article
        fields = ['title','text','image','category']
        labels = {
            'title': _('Please Enter Title'),
            
        }

        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter title'}),
            'text':forms.Textarea(attrs={'class':'form-control','placeholder':'Enter Body Text'})
            
        }

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['detail','profile_pic']


class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','rows':3,'column':10}))
    class Meta:
        model = Comment
        fields = ['comment']

