from django import forms

from apps.configuracion.empleado.models import Empleado

class EmpleadoForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([EmpleadoForm]): [Formulario de empleado]
    """    
    class Meta:
        model = Empleado
        exclude = ['is_active']
        widgets = {
            'nombre_emp' : forms.TextInput(attrs={'class':'form-control', 'name': 'nombre_emp', 
                'placeholder': 'Nombre del Empleado', 'required': 'required',
                'onkeyup':'aceptarLetras(this)', 'autocomplete': 'off','onchange': 'validateSpaceBlank(this)'}),
            'apellido_emp' : forms.TextInput(attrs={'class':'form-control', 'name': 'apellida_emp', 
                'placeholder': 'Apellido del Empleado', 'required': 'required',
                'onkeyup':'aceptarLetras(this)', 'autocomplete': 'off','onchange': 'validateSpaceBlank(this)'}),
            'ci_empe' : forms.TextInput(attrs={'class':'form-control', 'name':'apellido_emp', 
                'placeholder': 'Nro. Cédula', 'required':'required','onkeyup':'aceptarNumeros(this)', 
                'autocomplete': 'off','onchange': 'validateSpaceBlank(this)'}),
			'disponible' : forms.CheckboxInput(attrs={'class':'form-control', 'type': 'checkbox','name': 'disponible'}),
            'id_servicio' : forms.Select(attrs={'class':'form-control', 'id': 'id_servicio','required':'required' ,'name':'id_servicio'}),        
		}