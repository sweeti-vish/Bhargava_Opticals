import re
from django import forms
from django.contrib.auth.models import User
from .models import Customer


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=60, label='Your name')
    phone = forms.CharField(max_length=10, label='Mobile number (10 digits)')
    age = forms.IntegerField(required=False, min_value=1, max_value=120, label='Age (optional)')
    gender = forms.ChoiceField(
        choices=[('', 'Prefer not to say')] + Customer.GENDER,
        required=False, label='Gender (optional)')
    password = forms.CharField(widget=forms.PasswordInput, min_length=6, label='Password (at least 6 characters)')
    consent = forms.BooleanField(
        required=True,
        label='I agree to share these details with Bhargava Opticians')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not re.fullmatch(r'[6-9]\d{9}', phone):
            raise forms.ValidationError('Enter a valid 10-digit mobile number.')
        if User.objects.filter(username=phone).exists():
            raise forms.ValidationError('This number is already registered. Please log in.')
        return phone

