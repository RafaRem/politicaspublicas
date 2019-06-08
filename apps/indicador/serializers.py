from rest_framework import serializers
"""Modelos"""
from apps.indicador.models import *

class ConceptoGastoSerializer(serializers.ModelSerializer):
    clasificacion = serializers.SerializerMethodField('obtenerCategoria')
    class Meta:
        model=ConceptoGasto
        fields= '__all__'
    def obtenerCategoria(self,conceptoGasto):
        return conceptoGasto.clasificacion

class ClasifiacionGastoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClasificacionGasto
        fields = '__all__'