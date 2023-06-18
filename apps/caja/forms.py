from django import forms
from apps.caja.models import Caja

class CajaForm(forms.ModelForm):
    class Meta:
        model = Caja
        exclude = ['is_active']
        widgets = {
			'saldo_inicial' : forms.TextInput(attrs={'class':'form-control', 'name': 'saldo_inicial', 
                'placeholder': 'Monto Inicial Gs.', 'required': 'required','onkeyup':'aceptarNumeros(this)', 
                'autocomplete': 'off'}),
		}