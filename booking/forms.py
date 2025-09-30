from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service', 'date', 'time']
        labels = {
            'service': 'Serviço',
            'date': 'Data',
            'time': 'Hora',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {
            'username': 'Nome de utilizador',
            'email': 'Email',
            'password1': 'Palavra-passe',
            'password2': 'Confirmação da palavra-passe',
        }
        help_texts = {
            'username': 'Obrigatório. Máximo de 150 caracteres. Pode conter letras, números e os símbolos @ / . + - _.',
            'password1': (
                'A palavra-passe não pode ser demasiado semelhante às suas informações pessoais.<br>'
                'Deve conter pelo menos 8 caracteres.<br>'
                'Não pode ser uma palavra-passe comum.<br>'
                'Não pode ser composta apenas por números.'
            ),
            'password2': 'Introduza a mesma palavra-passe novamente para confirmação.',
        }