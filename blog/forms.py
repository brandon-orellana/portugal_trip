# blog/forms.py

from django import forms
from.models import PhotoContestSubmission, Comment

class PhotoContestForm(forms.Form):
    model = PhotoContestSubmission
    first_name = forms.CharField(label='First name', max_length=50)
    last_name = forms.CharField(label='Last name', max_length=50)
    email = forms.EmailField()
    photo = forms.ImageField()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'text']
        labels = {'name': 'Name', 'email': 'Email', 'text': 'Comment'}