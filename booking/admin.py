from django.contrib import admin
from .models import Booking, Service
from .models import CustomUser

admin.site.register(CustomUser)
# Register your models here.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)
    list_filter = ('name',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('service', 'user', 'date', 'time', 'status')
    list_filter = ('status', 'date')
    search_fields = ('service__name', 'user__username')