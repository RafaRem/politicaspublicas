from apps.programaOperativo.models import Acciones
from rest_framework import serializers

class AccionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acciones
        fields = '__all__'