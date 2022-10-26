from django import forms
from blog.models import Post


class ContactForm(forms.Form):

    name = forms.CharField(max_length=255)
    content = forms.CharField(widget=forms.Textarea)

class PostForm(forms.ModelForm):

    class Meta:
        model= Post
        fields = ('title', 'content', 'status', 'category', 'published_date')