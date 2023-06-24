from django import forms

from .models import Reserva

class ReservaForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([ReservaForm]): [Formulario de reservas]
    """   
    class Meta:
        model = Reserva
        exclude = ['is_active']
        widgets = {
			'descripcion' : forms.TextInput(attrs={'class':'form-control', 'name': 'descripcion', 
                                          'placeholder': 'Descripción de la reserva','onkeyup':'aceptarNumerosYLetras(this)',
                'autocomplete': 'off','onchange': 'validateSpaceBlank(this)'}),
            'fecha_reserva' :forms.HiddenInput(attrs={'id':'fecha_reserva'}),
            'hora_reserva' : forms.TextInput(attrs={'class':'form-control timepicker d-none', 'type': 'text',
                                                    'name':'hora_reserva','id':'hora_reserva' ,'required': 'required'}),
            'id_servicio' : forms.Select(attrs={'class':'form-control', 'id': 'id_servicio','required':'required' ,
                                                'name':'id_servicio'}),        
            'estado_re' : forms.Select(attrs={'class':'form-control', 'id': 'estado_re','required':'required' 
                                              ,'name':'estado_re'}),
            'color_estado' :forms.HiddenInput(),                
            'id_cliente' : forms.Select(attrs={'class':'form-control', 'id': 'id_cliente','required':'required' ,
                                               'name':'id_cliente'})
		}
