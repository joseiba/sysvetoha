from django import forms

from apps.inventario.depositos.models import Deposito

class DepositoForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([DepositoForm]): [Formulario de deposito]
    """    
    class Meta:
        model = Deposito
        fields = '__all__'
        labels = {
            'descripcion' : 'Descripción ',
        }
        widgets = {
			'descripcion' : forms.TextInput(attrs={'class':'form-control','autocomplete': 'off', 
            'name': 'descripcion', 'placeholder': 'Descripcion', 'required': 'required', 
            'onkeyup':'aceptarLetras(this)','onchange': 'validateSpaceBlank(this)'}),
		}