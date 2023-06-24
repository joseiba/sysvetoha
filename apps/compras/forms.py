from django import forms
from  apps.compras.models import Proveedor, Pedido, FacturaCompra, FacturaDet

replace_abc='replaceABC(this)'
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
                'autocomplete': 'off', 'placeholder': 'Nombre del Proveedor', 'required': 'required',
                'onkeyup':'replaceCaratect(this)', 'onchange': 'validateSpaceBlank(this)'}),		
			'direccion' : forms.TextInput(attrs={'class':'form-control','name': 'direccion', 'placeholder': 'Dirección',
                'onkeyup':'replaceDirection(this)','type':'text', 'required': 'required', 'autocomplete': 'off',
                'onchange': 'validateSpaceBlank(this)'}),
			'cedula' : forms.TextInput(attrs={'class':'form-control', 'name':'cedula', 'placeholder': 'Nro. Cédula', 
                'required':'required','onkeyup':replace_abc, 'autocomplete': 'off'}),
			'ruc_proveedor' : forms.TextInput(attrs={'class':'form-control', 'name': 'ruc_proveedor', 
                'placeholder': 'RUC', 'required': 'required','type':'text','onkeyup':replace_abc, 'autocomplete': 'off',
                'onchange': 'validateSpaceBlank(this)'}),
			'telefono' : forms.TextInput(attrs={'class':'form-control tel','placeholder': 'Telefono','type': 'tel', 
                'name':'telefono', 'required':'required','autocomplete': 'off','onkeyup':replace_abc,
                'pattern':'[^a-zA-Z\x22]+','title':'Evitar usar letras'}),
            'email' : forms.EmailInput(attrs={'class':'form-control optional', 'placeholder': 'Email','name':'email', 
                'type':'email', 'id':'email', 'autocomplete': 'off', 'onchange': 'validateSpaceBlank(this)'}),
		}

class PedidoForm(forms.ModelForm):
    """[summary]
    Args:
        forms ([PedidoForm]): [Formulario de pedidos]
    """    
    class Meta:
        model = Pedido
        exclude = ['is_active']
        widgets = {		
			'cantidad_pedido' : forms.TextInput(attrs={'class':'form-control', 'name':'cantidad_pedido', 
                                              'placeholder': 'Cantidad a pedir', 'required':'required','onkeyup':replace_abc}),
            'id_producto' : forms.Select(attrs={'class':'form-control', 'id': 'id_producto' ,'name':'id_producto', 
                                                'readonly': 'readonly'})
		}

class FacturaCompraForm(forms.ModelForm):
    
    class Meta:
        model = FacturaCompra
        exclude = ['is_active', 'estado']
        widgets = {
			'nro_factura': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off','name':'nro_factura',
                                         'placeholder': 'Escriba el nro de factura','required':'required','onkeyup':replace_abc, 
                                         'onchange': 'validateSpaceBlank(this)'}),
            'id_proveedor' : forms.Select(attrs={'class':'form-control', 'id': 'proveedor_select' ,'name':'id_proveedor'}),
            'fecha_emision_factura': forms.TextInput(attrs={'class': 'form-control',
                                            'id': 'datePick-emision-factura',
                                            'placeholder': 'Selecciona la fecha de emisión',
                                            'name':'fecha_emision_factura',
                                            'autocomplete': 'off'}),
            'fecha_emision': forms.TextInput(attrs={'class': 'form-control',
                                            'id': 'datePick-emision',
                                            'placeholder': 'Selecciona la fecha de inicio timbrado',
                                            'name':'fecha_emision',
                                            'autocomplete': 'off'}),
            'fecha_vencimiento': forms.TextInput(attrs={'class': 'form-control',
                                            'id': 'datePick-vencimiento',
                                            'placeholder': 'Selecciona la fecha de fin timbrado',
                                            'name':'fecha_vencimiento',
                                            'autocomplete': 'off'}),
            'nro_timbrado': forms.TextInput(attrs={'class': 'form-control', 'name': 'nro_timbrado','autocomplete': 'off',
                                                   'placeholder': 'Escriba el nro del timbrado','required':'required',
                                                   'onkeyup':replace_abc, 'onchange': 'validateSpaceBlank(this)'}),
		}


class FacturaDetalleForm(forms.ModelForm):
    class Meta:
        model = FacturaDet
        fields = ['id_pedido', 'cantidad']
        widgets = {
            'id_pedido': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'})
        }