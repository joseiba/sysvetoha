from django import forms
from apps.compras.models import Proveedor

class ProveedorForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([ClienteForm]): [Formulario de cliente]
    """    
    class Meta:
        model = Proveedor
        exclude = ['is_active']
        widgets = {
			'nombre_proveedor' : forms.TextInput(attrs={'class':'form-control','name': 'nombre_proveedor', 
                'autocomplete': 'off', 'placeholder': 'Nombre del Proveedor', 'required': 'required','onkeyup':'aceptarLetras(this)'}),		
			'direccion' : forms.TextInput(attrs={'class':'form-control','name': 'direccion', 'placeholder': 'Dirección',
                'onkeyup':'aceptarNumerosYLetras(this)','type':'text', 'required': 'required', 'autocomplete': 'off'}),
			'cedula' : forms.TextInput(attrs={'class':'form-control', 'name':'cedula', 'placeholder': 'Nro. Cédula', 
                'required':'required','onkeyup':'aceptarNumeros(this)', 'autocomplete': 'off'}),
			'ruc_proveedor' : forms.TextInput(attrs={'class':'form-control', 'name': 'ruc_proveedor', 
                'placeholder': 'RUC', 'required': 'required','type':'text','onkeyup':'aceptarNumeros(this)', 'autocomplete': 'off'}),
			'telefono' : forms.TextInput(attrs={'class':'form-control tel','placeholder': 'Telefono','type': 'tel', 
                'name':'telefono', 'required':'required','autocomplete': 'off','onkeyup':'aceptarNumeros(this)'}),
            'email' : forms.TextInput(attrs={'class':'form-control optional', 'placeholder': 'Email','name':'email', 
                'type':'email', 'id':'email', 'autocomplete': 'off'}),
		}