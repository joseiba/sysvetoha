from django import forms

from apps.cliente.models import Cliente, Ciudad

class CiudadForm(forms.ModelForm):
    class Meta:
        model = Ciudad
        exclude = ['is_active']
        widgets = {
			'nombre_ciudad' : forms.TextInput(attrs={'class':'form-control', 'name': 'nombre_ciudad', 
                'placeholder': 'Nombre de la Ciudad', 'required': 'required','onkeyup':'aceptarLetras(this)', 
                'autocomplete': 'off'}),
		}


class ClienteForm(forms.ModelForm):
    """[summary]
    Args:
        forms ([ClienteForm]): [Formulario de cliente]
    """    
    class Meta:
        model = Cliente
        exclude = ['is_active']
        widgets = {
			'nombre_cliente' : forms.TextInput(attrs={'class':'form-control','autocomplete': 'off',
                'name': 'nombre_cliente', 'placeholder': 'Nombre del Cliente', 'required': 'required','onkeyup':'aceptarLetras(this)'}),
			'apellido_cliente' : forms.TextInput(attrs={'class':'form-control','autocomplete': 'off', 'name': 'apellido_cliente', 
                'placeholder': 'Apellido del Cliente', 'required': 'required','onkeyup':'aceptarLetras(this)'}),
			'direccion' : forms.TextInput(attrs={'class':'form-control','name': 'direccion', 'placeholder': 'Dirección',
                'onkeyup':'aceptarNumerosYLetras(this)','type':'text', 'required': 'required', 'autocomplete': 'off'}),
			'cedula' : forms.TextInput(attrs={'class':'form-control', 'name':'cedula', 'placeholder': 'Nro. Cédula', 
                'required':'required','onkeyup':'aceptarNumeros(this)', 'autocomplete': 'off'}),
			'ruc' : forms.TextInput(attrs={'class':'form-control', 'name': 'ruc', 'placeholder': 'RUC', 'type':'text',
                'onkeyup':'aceptarNumeros(this)', 'autocomplete': 'off'}),
			'telefono' : forms.TextInput(attrs={'class':'form-control tel','placeholder': 'Telefono','type': 'tel', 
            'name':'telefono', 'required':'required','onkeyup':'aceptarNumeros(this)', 'autocomplete': 'off'}),
            'email' : forms.TextInput(attrs={'class':'form-control optional', 'placeholder': 'Email','name':'email', 
                'type':'email', 'id':'email', 'autocomplete': 'off'}),
            'id_ciudad' : forms.Select(attrs={'class':'form-control', 'id': 'id_ciudad','required':'required' ,'name':'id_ciudad',
            'autocomplete': 'off'})
		}