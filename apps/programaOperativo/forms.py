from apps.programaOperativo.models import ProgramaOperativo
from django import forms

class ProgramaOperativoForm(forms.ModelForm):
    class Meta:
        model = ProgramaOperativo
        fields = '__all__'
        exclude = ('nombre','objetivo', 'dependencia',)
    def __init__(self, *args, **kwargs):
        super(ProgramaOperativoForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True 
    