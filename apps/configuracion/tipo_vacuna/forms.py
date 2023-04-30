
from django import forms

from apps.configuracion.tipo_vacuna.models import TipoVacuna

class TipoVacunaForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([TipoVacunaForm]): [Formulario de vacunas]
    """    
    class Meta:
        model = TipoVacuna
        fields = '__all__'        
        widgets = {
            'id_producto' : forms.Select(attrs={'class':'form-control', 'id': 'id_producto' ,'name':'id_producto', 'readonly': 'readonly', 
                'onfocus': 'this.size=5;', 'onblur': 'this.size=1;', 'onchange': 'this.size=1; this.blur();'}),
            'nombre_vacuna' : forms.TextInput(attrs={'class':'form-control', 'name': 'nombre_vacuna', 'placeholder': 'Vacuna Dosis', 'required': 'required','autocomplete': 'off','onkeyup':'aceptarLetras(this)'}),
            'periodo_aplicacion' : forms.TextInput(attrs={'class':'form-control', 'name': 'periodo_aplicacion', 'placeholder': 'Periodo de Aplicacion', 
                'required': 'required','autocomplete': 'off'  ,'onkeyup':'aceptarNumeros(this)'}),
            'multi_aplicaciones' : forms.Select(attrs={'class':'form-control', 'id': 'multi_aplicaciones','required':'required' ,'name':'multi_aplicaciones'}),
		}
        