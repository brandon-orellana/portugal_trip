# blog/forms.py

from django import forms
from.models import PhotoContestSubmission
class PhotoContestForm(forms.Form):
    model = PhotoContestSubmission
    first_name = forms.CharField(label='First name', max_length=50)
    last_name = forms.CharField(label='Last name', max_length=50)
    email = forms.EmailField()
    photo = forms.ImageField()