from apps.programaOperativo.models import ProgramaOperativo, Actividad
from django import forms

class ProgramaOperativoForm(forms.ModelForm):
    class Meta:
        model = ProgramaOperativo
        fields = '__all__'
        exclude = ['acciones','estado',]
    def __init__(self, *args, **kwargs):
        super(ProgramaOperativoForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs['readonly'] = True 
            self.fields[key].widget.attrs['disabled'] = True 

class ActividadesForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = '__all__'
        exclude = [
            'programaoperativo',
            'personasInvolucradas',
            'beneficiarios',
            'evidencia',
            'user',
            'latitud',
            'longitud',
            'accion',
            'fecha_in',
            'fecha_fi',
            'estado'
        ]

class TerminarActividadesForm(forms.ModelForm):
    class Meta:
        model=Actividad
        fields = [            
            'personasInvolucradas',
            'beneficiarios'
            ]
        exclude = [
            'programaoperativo',
            'evidencia',
            'user',
            'latitud',
            'longitud',
            'accion',
            'fecha_in',
            'fecha_fi'
        ]
        pass
    def __init__(self, *args, **kwargs):
        super(TerminarActividadesForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True 
    