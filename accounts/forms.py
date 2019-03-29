from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'name', 'gendar'
        )

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'gendar')


class ContactForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField
    message = forms.CharField(widget=forms.Textarea) # 問い合わせ内容

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'お名前'
