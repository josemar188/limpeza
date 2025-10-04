"""
URL configuration for Limpeza project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from booking import views
from booking import urls as booking_urls
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from booking.views import signup_view
from booking.views import login_error_view
from booking.views import contact_view
from django.views.generic import TemplateView




 
app_name = 'booking'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api', include('booking.urls')),
    path('booking', views.book_service, name='book_service'),  
    path('history/', views.booking_history, name='bookings_list'),

    path('history/<int:booking_id>/', views.confirmar_reserva, name='confirmar-reserva'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile/edit/', views.edit_profile, name='edit_profile'),
    path('accounts/profile/change_password/', views.change_password, name='change_password'),
    path('accounts/profile/delete/', views.delete_account, name='delete_account'),
    
    path('servicos/', views.service_list, name='servicos'),
    path('', views.home, name='home' ),
    path('signup/', signup_view, name='signup'),
    path('accounts/', include('allauth.urls')),
    path('login-error/', login_error_view),

    path('contact/', contact_view, name='contact'),
    path('contact/success/', TemplateView.as_view(template_name='booking/contact_success.html'), name='contact_success'),
]