from django import forms
from .models import Post


class PostNewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'postCategory',
            'categoryType',
            'title',
            'text',
        ]


class PostArticleForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'postCategory',
            'categoryType',
            'title',
            'text',
        ]
