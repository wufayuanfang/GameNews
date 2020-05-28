from django import forms
from .models import Comment_vidoe


class Comment_vidoeForm(forms.ModelForm):
    class Meta:
        model = Comment_vidoe
        fields = {'text'}
