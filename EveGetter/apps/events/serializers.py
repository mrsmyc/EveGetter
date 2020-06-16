from rest_framework import serializers
from .models import Event


class EventSerializers(serializers.ModelSerializer):
    class Meta:
        model = Event
        fiels = ('event_type', 'age_start', 'date',)