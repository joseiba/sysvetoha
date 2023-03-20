from django import forms

from .models import Especie, Raza

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
            'nombre_especie' : forms.TextInput(attrs={'class':'form-control','onkeyup':'raceptarLetras(this)' ,'id': 'nombre_especie',
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
