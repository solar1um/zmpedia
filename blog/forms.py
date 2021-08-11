from django import forms
from blog.models import Post, Comment


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'image', 'post']


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'image', 'post']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'text')
