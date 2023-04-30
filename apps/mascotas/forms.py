from django import forms

from .models import Especie, Mascota, Raza, FichaMedica, Vacuna, Consulta, Antiparasitario

class EspecieForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([EspecieForm]): [Formulario de Especie]
    """    
    class Meta:
        model = Especie
        fields = '__all__'  
        labels = {
            'nombre_especie' : 'Nombre Especie ',
        }     
        widgets = {
            'nombre_especie' : forms.TextInput(attrs={'class':'form-control','onkeyup':'aceptarLetras(this)' ,'id': 'nombre_especie',
                'name': 'nombre_especie', 'placeholder': 'Nombre de la Especie', 'required': 'required',  'autocomplete': 'off',}),
		}


class RazaForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([RazaForm]): [Formulario de Raza]
    """    
    class Meta:
        model = Raza
        fields = '__all__' 
        labels = {
            'nombre_especie' : 'Especie ',
            'nombre_raza' : 'Nombre Raza ',
        }        
        widgets = {
            'nombre_raza' : forms.TextInput(attrs={'class':'form-control', 'id': 'nombre_raza','autocomplete': 'off',
                'name': 'nombre_raza','onkeyup':'aceptarLetras(this)','placeholder': 'Nombre de la Raza', 'required': 'required'}),
            'id_especie' : forms.Select(attrs={'class':'form-control', 'id': 'id_especie','required':'required' ,'name':'id_especie'}),
		}        


class MascotaForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([MascotaForm]): [Formulario de la mascota]
    """    
    class Meta:
        model = Mascota
        fields = '__all__'   
        widgets = {
            'nombre_mascota': forms.TextInput(attrs={'class':'form-control', 'name': 'nombre_mascota',
                'onkeyup':'aceptarLetras(this)','placeholder': 'Nombre de la mascota', 'required': 'required','autocomplete': 'off'}),
            'tatuaje': forms.TextInput(attrs={'class':'form-control optional', 'onkeyup':'aceptarLetras(this)',
                'name': 'tatuaje', 'placeholder': 'Tatuaje', 'autocomplete': 'off'}),
            'edad': forms.TextInput(attrs={'class':'form-control optional', 'name': 'edad', 'placeholder': 'Edad',
                'onkeyup':'aceptarNumeros(this)', 'autocomplete': 'off'}),
            'sexo' : forms.Select(attrs={'class':'form-control', 'id': 'sexo','required':'required' ,'name':'sexo', 'autocomplete': 'off'}),
            'fecha_nacimiento' : forms.TextInput(attrs={'class':'form-control optional date', 'type': 'date',
                'name':'fecha_nacimiento','autocomplete': 'off'}),
            'peso': forms.TextInput(attrs={'class':'form-control','onkeyup':'aceptarNumeros(this)', 'name': 'peso', 
                'placeholder': 'Peso', 'required': 'required', 'autocomplete': 'off'}),
            'color_pelaje' : forms.TextInput(attrs={'class':'form-control', 'type': 'color','name':'color_pelaje',
                'placeholder': 'Color Pelaje', 'autocomplete': 'off'}),
            'imagen': forms.FileInput(attrs={'type': 'file', 'name':'imagen', 'id': 'imageInput', 'accept':'image/*'}),
            'id_raza' : forms.Select(attrs={'class':'form-control', 'id': 'id_raza','required':'required' ,'name':'id_raza', 'autocomplete': 'off'}),
            'id_cliente' : forms.Select(attrs={'class':'form-control', 'id': 'id_cliente','required':'required' ,'name':'id_cliente', 'autocomplete': 'off'})
		}

class FichaMedicaForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([FichaMedicaForm]): [Formulario de Ficha de Medica]
    """ 
    class Meta:
        model = FichaMedica
        exclude = ['fecha_create']
        widgets = {
        'id_mascota' : forms.HiddenInput(),
        }


class VacunaForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([VacunaForm]): [Formulario de Vacuna]
    """ 
    class Meta:
        model = Vacuna
        fields = '__all__'   
        widgets = {
        'proxima_vacuna' : forms.Select(attrs={'class':'form-control', 'id': 'id_vacuna','name':'proxima_vacuna'}),
        'id_vacuna' : forms.Select(attrs={'class':'form-control', 'id': 'id_vacuna','name':'id_vacuna'}),
        'fecha_aplicacion': forms.TextInput(attrs={'class': 'form-control',
                                            'id': 'datePick-aplicacion',
                                            'placeholder': 'Fecha Aplicacion',
                                            'name':'fecha_aplicacion',
                                            'autocomplete': 'off',
                                            'readonly': "readonly",
                                            'disabled': 'disabled'}),
        'fecha_proxima_aplicacion': forms.TextInput(attrs={'class': 'form-control',
                                            'id': 'datePick-proxima-aplicacion',
                                            'placeholder': 'Proxima Aplicacion',
                                            'name':'fecha_proxima_aplicacion',
                                            'readonly': "readonly",
                                            'disabled': 'disabled',
                                            'autocomplete': 'off'}),
        'id_ficha_medica' : forms.HiddenInput(),        
        }


class ConsultaForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([ConsultaForm]): [Formulario de Consulta]
    """ 
    class Meta:
        model = Consulta
        fields = '__all__'   
        widgets = {
        'diagnostico': forms.Textarea(attrs={'class':'form-control optional','name': 'diagnostico', 
                                             'rows': '2','placeholder': 'Diagnostico','onkeyup':'aceptarLetras(this)'}),
        'tratamiento': forms.Textarea(attrs={'class':'form-control optional', 'rows': '2', 'name': 'tratamiento', 
                                             'placeholder': 'Tratamiento','onkeyup':'aceptarLetras(this)'}),
        'medicamento': forms.Textarea(attrs={'class':'form-control optional', 'rows': '2', 'name': 'medicamento', 
                                             'placeholder': 'Medicamento','onkeyup':'aceptarLetras(this)'}),
        'proximo_tratamiento' : forms.Textarea(attrs={'class':'form-control optional', 'rows': '2', 'type': 'text',
                                                      'name':'proximo_tratamiento','onkeyup':'aceptarLetras(this)'}),
        'id_ficha_medica' : forms.HiddenInput(),
        }
        

class AntiparasitarioForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([AntiparasitarioForm]): [Formulario de Antiparasitario]
    """ 
    class Meta:
        model = Antiparasitario
        fields = '__all__'   
        widgets = {
        'antiparasitario': forms.TextInput(attrs={'class':'form-control optional', 'name': 'antiparasitario', 
                                                  'placeholder': 'Antiparasitario','onkeyup':'aceptarNumerosYLetras(this)'}),
        'proximo_antiparasitario' : forms.TextInput(attrs={'class':'form-control optional', 'type': 'text',
                                                           'name':'proximo_antiparasitario','onkeyup':'aceptarNumerosYLetras(this)'}),  
        'id_ficha_medica' : forms.HiddenInput(),
        }
                