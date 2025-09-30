from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='service.name', read_only=True)
    start = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ['id', 'title', 'start', 'status']

    def get_start(self, obj):
        return f"{obj.date}T{obj.time}"