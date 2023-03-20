from django import forms

from apps.configuracion.servicio.models import Servicio

class ServicioForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([ServicioForm]): [Formulario de servicios]
    """    
    class Meta:
        model = Servicio
        exclude = ['is_active']
        widgets = {
            'cod_serv' : forms.TextInput(attrs={'class':'form-control', 'name': 'cod_serv', 'placeholder': 'Nombre del Servicio', 
                'autocomplete': 'off','required': 'required','onkeyup':'aceptarLetras(this)'}),
			'nombre_servicio' : forms.TextInput(attrs={'class':'form-control','autocomplete': 'off', 'name': 'nombre_servicio',
                'placeholder': 'Nombre del Servicio', 'required': 'required','onkeyup':'aceptarLetras(this)'}),
			'precio_servicio' : forms.TextInput(attrs={'class':'form-control', 'name': 'precio_servicio', 
                'placeholder': 'Precio del Servicio', 'autocomplete': 'off','required': 'required','onkeyup':'aceptarNumeros(this)'}),
            'min_serv' : forms.TextInput(attrs={'class':'form-control', 'name': 'min_serv', 
                'placeholder': 'Tiempo del servicio en minutos', 'autocomplete': 'off','required': 'required','onkeyup':'aceptarNumeros(this)'})
		}