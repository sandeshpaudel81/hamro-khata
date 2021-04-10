from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Party, Transaction

class RegisterForm(UserCreationForm):
    
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True, help_text='Enter a valid email address!')

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'address',
            'birth_date',
        ]

class PartyForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = [
            'name',
            'address',
            'contact',
        ]

class TransactionForm(forms.ModelForm):
    ACTION_CHOICES = [
        ('add', '+'),
        ('sub', '-'),
    ]

    action = forms.ChoiceField(choices=ACTION_CHOICES, label="To Pay/To get", help_text="Choose + for income and - for expense")

    class Meta:
        model = Transaction
        fields = [
            'party',
            'action',
            'amount',
            'description',
            'datetime',
        ]