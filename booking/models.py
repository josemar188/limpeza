from django.db import models
from django.contrib.auth.models import User

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=SERVIVE_STATUS, default='PENDENTE')
    collaborator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='collaborator_bookings')
    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'

    def __str__(self):
        return f"{self.service.name} on {self.date} at {self.time}"
