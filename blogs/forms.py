from django import forms

from blogs.models import Blog
from main.forms import StyleForm

class BlogCreateForm(StyleForm, forms.ModelForm):

    class Meta:
        model = Blog
        fields = ('image', 'title', 'body')
