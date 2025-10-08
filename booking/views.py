from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BookingForm
from .models import Booking
from .serializers import BookingSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserCreationForm
from django.http import HttpResponse
from booking.forms import ContactForm
from django.core.mail import EmailMessage
from .forms import CustomUserForm
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver



# Create your views here.
class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)







@login_required
def book_service(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()

            confirmation_url = request.build_absolute_uri(
                reverse('confirmar-reserva', args=[booking.id])
            )
            collaborator_name = booking.collaborator.name if booking.collaborator else 'Não atribuído'
            # Send email to me
            email = EmailMessage(
                subject=f'Nova reserva: {booking.service.name}',
                body=(
                    f"Reserva para o serviço de {booking.service.name} em {booking.date} às {booking.time}.\n"
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

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('bookings_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = BookingForm()
    return render(request, 'booking/book_service.html', {'form': form})












def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-date', '-time')
    return render(request, 'booking/bookings_list.html', {'bookings': bookings})

def confirmar_reserva(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'CONFIRMADO'
    booking.save()
    messages.success(request, 'Reserva confirmada com sucesso!')
    return redirect('booking_history')






#registration and profile management views
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book_service')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
@login_required
def profile(request):
    return render(request, 'registration/profile.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('profile')
    else:
        form = CustomUserForm(instance=request.user)
    return render(request, 'registration/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Senha alterada com sucesso!')
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form})
@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Conta deletada com sucesso!')
        return redirect('book_service')
    return render(request, 'registration/delete_account.html')


def validate_morada(morada):
    url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': morada,
        'format': 'json',
        'addressdetails': 1,
        'limit': 1
    }
    response = requests.get(url, params=params)
    data = response.json()
    if not data:
        raise ValidationError('Morada inválida ou não encontrada.')





def service_list(request):
    services = BookingForm().fields['service'].queryset
    return render(request, 'booking/servicos.html', {'services': services})

def home(request):
    return render(request, 'booking/home.html')


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # ou para onde quiser
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def login_error_view(request):
    return HttpResponse("Erro de login social. Verifique credenciais e redirecionamento.")



def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()

            # Envia email de confirmação
            send_mail(
                subject='Confirmação de contacto - TACE Cleaning',
                message=f"Olá {contact.nome},\n\nRecebemos sua mensagem e entraremos em contacto em breve.\n\nMensagem enviada:\n{contact.mensagem}",
                from_email='noreply@espacolimpo.com',
                recipient_list=[contact.email],
                fail_silently=False,
            )

            return redirect('contact_success')
    else:
        form = ContactForm()

    return render(request, 'booking/contacto.html', {'form': form})
