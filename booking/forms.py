from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from booking.models import Booking
from .models import ContactMessage
from django.utils import timezone


class BookingForm(forms.ModelForm):
    mensagem = forms.CharField(
            label='Mensagem',
            widget=forms.Textarea(attrs={'rows': 4}),
            required=False
        )

    class Meta:
        model = Booking
        fields = ['service', 'date', 'time', 'mensagem']
        labels = {
            'service': 'Serviço',
            'date': 'Data',
            'time': 'Hora',
            'mensagem': 'Mensagem',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean_date(self):
        data = self.cleaned_data['date']
        if data < timezone.localdate():
            raise forms.ValidationError("A data não pode ser no passado.")
        return data

    def clean_time(self):
        hora = self.cleaned_data['time']
        if hora.hour < 6 or hora.hour > 23:
            raise forms.ValidationError("Escolha um horário entre 06:00 e 00:00.")
        return hora
    


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


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['nome', 'email', 'telefone', 'mensagem']
        labels = {
            'nome': 'Nome',
            'email': 'Email',
            'telefone': 'Telefone',
            'mensagem': 'Mensagem',
        }
        widgets = {
            'mensagem': forms.Textarea(attrs={'rows': 4}),
        }