from apps.programaOperativo.models import ProgramaOperativo, Actividad
from django import forms

class ProgramaOperativoForm(forms.ModelForm):
    class Meta:
        model = ProgramaOperativo
        fields = '__all__'
        exclude = ('nombre','objetivo', 'dependencia', 'acciones',)
    def __init__(self, *args, **kwargs):
        super(ProgramaOperativoForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True 

class ActividadesForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = '__all__'
        exclude = [
            'programaoperativo',
            'presupuestoEjercido',
            'personasInvolucradas',
            'evidencia',
            'user',
            'latitud',
            'longitud',
            'accion'
        ]

class TerminarActividadesForm(forms.ModelForm):
    class Meta:
        model=Actividad
        fields = [            
            'presupuestoEjercido',
            'personasInvolucradas',
            ]