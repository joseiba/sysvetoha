from django.contrib.auth.forms import AuthenticationForm,  UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import Group, Permission
from django.forms import *
from django import forms

from apps.usuario.models import User

class FormLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FormLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'input100'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
        self.fields['password'].widget.attrs['class'] = 'input100'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'


class UserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):        
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['groups'].widget.attrs['class'] = 'group_select'
        self.fields['groups'].widget.attrs['required'] = 'required'
        self.fields['groups'].widget.attrs['style'] = 'width: 100%'


    class Meta():
        model = User
        fiels = ("first_name", "last_name", "email", "username", "groups", "password1", "password2")
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control','name': 'first_name', 'placeholder': 'Ingrese el nombre del usuario','onkeyup':'aceptarLetras(this)', 'required': 'required', 
                    'autocomplete':"off",'onchange': 'validateSpaceBlank(this)'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control','name': 'last_name', 'placeholder': 'Ingrese el apellido del usuario','onkeyup':'aceptarLetras(this)', 
                    'required': 'required', 'autocomplete':"off",'onchange': 'validateSpaceBlank(this)'
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'class':'form-control optional', 'placeholder': 'Email','name':'email', 'type':'email', 
                    'id':'email', 'autocomplete':"off",'onchange': 'validateSpaceBlank(this)'
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control','name': 'username', 'placeholder': 'Nombre de usuario','onkeyup':'aceptarNumerosYLetras(this)', 
                    'required': 'required', 'autocomplete':"off",'onchange': 'validateSpaceBlank(this)'
                }
            ),
        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff', 'password', 'profile']
        help_texts = {
					'username' : None,
                    'email': None,
                    'first_name': None,
                    'last_name': None,
                    'password1': None,
                    'password2': None,
					} 

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        for grupo in self.cleaned_data['groups']:
            user.groups.add(grupo)
        return user


class UserFormChange(UserChangeForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user        
        super().__init__(*args, **kwargs)
        self.fields['groups'].widget.attrs['class'] = 'group_select'
        self.fields['groups'].widget.attrs['required'] = 'required'
        self.fields['groups'].widget.attrs['style'] = 'width: 100%'

        for fieldname in ['username']:
            self.fields[fieldname].help_text = None

        try:
            if not self.user.has_perms(['usuario.change_user']):
                for fieldname in ['groups']:
                    self.fields[fieldname].widget.attrs['class'] = 'd-none'
                    self.fields[fieldname].label = ''
                    self.fields[fieldname].help_text = None
        except:
            pass

    password = None

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "groups")
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control','name': 'first_name', 'placeholder': 'Ingrese el nombre del usuario','onkeyup':'aceptarLetras(this)', 
                    'required': 'required', 'autocomplete':"off",'onchange': 'validateSpaceBlank(this)'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control','name': 'last_name', 'placeholder': 'Ingrese el apellido del usuario','onkeyup':'aceptarLetras(this)', 
                    'required': 'required', 'autocomplete':"off",'onchange': 'validateSpaceBlank(this)'
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'class':'form-control optional', 'placeholder': 'Email','name':'email', 'type':'email', 
                    'id':'email', 'autocomplete':"off",'onchange': 'validateSpaceBlank(this)'
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control','name': 'username', 'placeholder': 'Nombre de usuario','onkeyup':'aceptarNumerosYLetras(this)', 
                    'required': 'required', 'autocomplete':"off",'onchange': 'validateSpaceBlank(this)'
                }
            ),
        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff', 'password','profile']

        help_texts = {
					'username' : None,
                    'email': None,
                    'first_name': None,
                    'last_name': None,
                    'password': None,
					} 


    def save(self, commit=True):
        form = super()
        if form.is_valid():
            user = form.save(commit=False)
            user.groups.clear()
            for grupo in self.cleaned_data['groups']:
                user.groups.add(grupo)
            return user


queryset = [
    "user",
    "producto",
    "especie",
    "raza",
    "cliente",
    "mascota",
    "reserva",
    "confiempresa",
    "servicio",
    "empleado",
    "facturacompra",
    "proveedor",
    "pedidocabecera",
    "cabeceraventa",
    "inventario",
    "tipovacuna",
    "reporte",
    "caja"
]

class GroupForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['permissions'].queryset = Permission.objects.filter(content_type__model__in=queryset)

    class Meta:
        model = Group
        fields = ('name', 'permissions')
        widgets = {
            'name': forms.TextInput(attrs={
                'class':'form-control', 'autocomplete': 'off',
                'placeholder':'Agregar nombre del rol' ,'onchange': 'validateSpaceBlank(this)'
            }),
            'permissions': forms.CheckboxSelectMultiple(),
        }


class GroupChangeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['permissions'].queryset = Permission.objects.filter(content_type__model__in=queryset)
    
    class Meta:
        model = Group
        fields = ('name', 'permissions')
        widgets = {
            'name': forms.TextInput(attrs={
                'class':'form-control', 'autocomplete': 'off',
            }),
            'permissions': forms.CheckboxSelectMultiple(),
        }


class ContraseñaChangeForm(PasswordChangeForm):

    def __init__(self , user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['old_password'].widget.attrs['required'] = 'required'
        self.fields['new_password1'].widget.attrs['required'] = 'required'
        self.fields['new_password2'].widget.attrs['required'] = 'required'

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError("La contraseña actual no coinciden!")
        return old_password