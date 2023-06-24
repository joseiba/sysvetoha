from django import forms

from apps.configuracion.configuracion_inicial.models import ConfiEmpresa

class ConfiEmpresaForm(forms.ModelForm):
    class Meta:
        model = ConfiEmpresa
        exclude = ['id_confi']
        widgets = {
            'nombre_empresa' : forms.TextInput(attrs={'class':'form-control', 'autocomplete': 'off','name': 'nombre_empresa', 'placeholder': 'Nombre de la empresa', 'required': 'required',
                                                      'onkeyup':'aceptarLetras(this)', 'onchange': 'validateSpaceBlank(this)'}),
            'direccion' : forms.TextInput(attrs={'class':'form-control', 'autocomplete': 'off','name': 'direccion', 'placeholder': 'Direccion de la empresa', 'required': 'required','onkeyup':'aceptarNumerosYLetras(this)',
                                                 'onchange': 'validateSpaceBlank(this)'}),
            'cuidad' : forms.TextInput(attrs={'class':'form-control', 'autocomplete': 'off','name': 'cuidad', 'placeholder': 'Cuidad de la empresa', 'required': 'required',
                                              'onkeyup':'aceptarLetras(this)', 'onchange': 'validateSpaceBlank(this)'}),
            'telefono' : forms.TextInput(attrs={'class':'form-control', 'autocomplete': 'off','name': 'telefono', 'placeholder': 'Telefono de la empresa', 'required': 'required',
                                                'onkeyup':'aceptarNumeros(this)', 'onchange': 'validateSpaceBlank(this)'}),
            'fecha_inicio_timbrado': forms.TextInput(attrs={'class': 'form-control',
                                            'id': 'datePick-emision',
                                            'placeholder': 'Selecciona la fecha de inicio',
                                            'name':'fecha_inicio_timbrado',
                                            'autocomplete': 'off',
                                            'required': 'required'}),
            'fecha_fin_timbrado': forms.TextInput(attrs={'class': 'form-control',
                                            'id': 'datePick-vencimiento',
                                            'placeholder': 'Selecciona la fecha de vencimiento',
                                            'name':'fecha_fin_timbrado',
                                            'autocomplete': 'off',
                                            'required': 'required'}),
            'nro_timbrado': forms.TextInput(attrs={'class': 'form-control', 'name': 'nro_timbrado','id':'nro_timbrado','autocomplete': 'off',
                                                   'placeholder': 'Escriba el nro del timbrado','required':'required','onkeyup':'aceptarNumeros(this)',
                                                   'onchange': 'validateSpaceBlank(this)'}),
            'ruc_empresa': forms.TextInput(attrs={'class': 'form-control', 'name': 'ruc_empresa','autocomplete': 'off','placeholder': 'Escriba el RUC','required':'required',
                                                  'onkeyup':'aceptarNumeros(this)','onchange': 'validateSpaceBlank(this)'}),
            'apertura_caja_inicial' : forms.TextInput(attrs={'class':'form-control', 'autocomplete': 'off',
                                                             'name': 'apertura_caja_inicial', 'placeholder': 'Ingrese el monto inicial de la caja', 'required': 'required','onkeyup':'aceptarNumeros(this)'
                                                             ,'onchange': 'validateSpaceBlank(this)'}),
			'ubicacion_deposito_inicial' : forms.TextInput(attrs={'class':'form-control', 'autocomplete': 'off','name': 'ubicacion_deposito_inicial', 'placeholder': 'Deposito inicial', 
                                                         'required': 'required','onkeyup':'aceptarLetras(this)'
                                                         ,'onchange': 'validateSpaceBlank(this)'}),
            'dias_a_vencer' : forms.TextInput(attrs={'class':'form-control', 'autocomplete': 'off','name': 'dias_a_vencer', 'placeholder': 'Dias Productos a Vencer', 'required': 'required','onkeyup':'aceptarNumeros(this)'}),
            'dias_alert_vacunas' : forms.TextInput(attrs={'class':'form-control', 'autocomplete': 'off','name': 'dias_alert_vacunas', 'placeholder': 'Dias aviso proximas vacunaciones', 'required': 'required','onkeyup':'aceptarNumeros(this)'}),
            'nro_sucursal' : forms.TextInput(attrs={'class':'form-control', 'autocomplete': 'off','name': 'nro_sucursal', 'required': 'required','onkeyup':'aceptarNumeros(this)'}),
            'nro_caja' : forms.TextInput(attrs={'class':'form-control', 'autocomplete': 'off','name': 'nro_caja', 'required': 'required','onkeyup':'aceptarNumeros(this)'}),
            'nro_factura' : forms.TextInput(attrs={'class':'form-control', 'autocomplete': 'off','name': 'nro_factura','required': 'required','onkeyup':'aceptarNumeros(this)'}),

		}