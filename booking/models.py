from django.db import models
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.contrib.auth.models import AbstractUser,  Group, Permission 
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name='Serviço')
    description = models.TextField(blank=True, verbose_name='Descrição')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço')
    duration = models.DurationField(verbose_name='Duração')

    def __str__(self):
        return self.name
    





class Booking(models.Model):
    SERVIVE_STATUS = [
        ('PENDENTE', 'Pendente'),
        ('CONFIRMADO', 'Confirmado'),
        ('CANCELADO', 'Cancelado'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings_as_user')
    collaborator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings_as_collaborator')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    morada = models.CharField(max_length=255, blank=True)
    mensagem = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=SERVIVE_STATUS, default='PENDENTE')
    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'

    def __str__(self):
        return f"{self.service.name} on {self.date} at {self.time}"







def contact_view(request):
    if request.method == 'POST':
        booking = form.save(commit=False)
        booking.user = request.user
        booking.save()

        confirmation_url = request.build_absolute_uri(
            reverse('confirmar-reserva', args=[booking.id])
        )
        collaborator_name = booking.collaborator.name if booking.collaborator else 'Não atribuído'

        # Envia email de confirmação
        email = EmailMessage(
            subject=f'Nova reserva: {booking.service.name}',
            body=(
                f"Reserva para o serviço de {booking.service.name} para {booking.date} às {booking.time}.\n"
                f"Cliente: {booking.user.username}\n"
                f"Email do cliente: {booking.user.email}\n"
                f"Colaborador: {collaborator_name}\n"
                f"Confirme a reserva: {confirmation_url}"
            ),
            from_email='jusng188@gmail.com',
            to=['jusng188@gmail.com'],
            reply_to=[booking.user.email],
        )
        email.send()

        return redirect('contact_success')
    else:
        form = ContactForm()

    return render(request, 'booking/contact.html', {'form': form})


class ContactMessage(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    mensagem = models.TextField()
    enviado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} ({self.email})"
    

class CustomUser(AbstractUser):
    morada = models.CharField(max_length=255, blank=True, null=True)
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )