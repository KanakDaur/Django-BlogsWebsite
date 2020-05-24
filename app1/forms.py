from django import forms
from django.contrib.auth.models import User
from app1.models import comment,post,Profile
class signupform(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password','email','first_name','last_name']


class commentform(forms.ModelForm):
    class Meta:
        model = comment
        fields = ('content',)

class Usereditform(forms.ModelForm):
    username = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'})) # means it is not editable after once created
    email = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'})) # means it is not editable after once created
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name')

class Profileeditform(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
