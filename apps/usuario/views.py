import math
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.models import Group

from apps.usuario.forms import FormLogin, UserForm, UserFormChange, GroupForm, GroupChangeForm, ContraseñaChangeForm
from apps.usuario.models import User
from apps.configuracion.configuracion_inicial.models import ConfiEmpresa
from apps.utiles.views import *
from apps.caja.models import Caja

# Create your views here.
date_time = datetime.now()
today = date_time.strftime("%d/%m/%Y")

class Login(FormView):
    """[summary]
    Args:
        FormView ([Login]): [clase que ingresa al login]
    Returns:
        [Login]: [Retorna el index si esta autenticado o si no al login]
    """    
    template_name = 'registration/login.html'
    form_class = FormLogin
    success_url = reverse_lazy('index')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self,request,*args, **kwargs):    
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']
                usuario = authenticate(username=username, password=password)
                if usuario is None: 
                    messages.error(request,'El nombre de usuario y/o contraseña son incorrectos')         
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self,form):
        login(self.request,form.get_user())
        confi = ConfiEmpresa.objects.filter()
        if confi.count() == 0:
            confi_initial = ConfiEmpresa()
            confi_initial.id = 1
            confi_initial.save()
        return super(Login,self).form_valid(form)

@login_required()
def logoutUser(request):
    """[summary]
    Args:
        request ([Logout]): [Metodo herado de logout de django para cerrar sesión]
    Returns:
        [Redirect template]: [Retorna el template del login]
    """    
    logout(request)
    return redirect('/accounts/login/')

@login_required()
def home_user(request):
    """[summary]
    Args:
        request ([Respuesta del index]): [Nombre de donde va ir redirigido]
    Returns:
        [Render template]: 
        [
            Se utiliza el metodo render, con los campos del request, y directorio
            de donde se encuentra el template            
        ]
        """  
    caja_abierta = Caja.objects.exclude(apertura_cierre="C").filter(fecha_alta=today)
    if caja_abierta.count() == 0:
        messages.success(request, 'Se debe realizar la apertura de caja para hacer los registros de facturas.')

    context = {
        'total_user': total_user(),
        'total_cliente': total_cliente(),
        'total_mascotas': total_mascotas(),
        'total_productos': total_producto(),
        'total_stock_minimo': total_stock_minimo(),
        'total_pro_vencer': total_productos_a_vencer(),
        'total_vacunas_aplicadas' : total_vacunas_aplicadas(),
        'total_reservas_hoy': total_reservas_hoy(),
        'total_proximas_vacunas': total_vacunas_proximas()
    }
    return render(request, "home/index.html", context)    


@login_required()
@permission_required('usuario.view_user')
def list_usuarios(request):    
    return render(request, "usuario/list_usuarios.html")

@login_required()
def list_usuarios_ajax(request):
    query = request.GET.get('busqueda')
    if query:
        usuario = User.objects.exclude(is_active=False).filter(Q(first_name__icontains=query) 
            | Q(last_name__icontains=query) | Q(username__icontains=query))
        usuario = usuario.exclude(is_superuser=True)
    else:
        usuario = User.objects.exclude(is_active=False).all()
        usuario = usuario.exclude(is_superuser=True)

    total = usuario.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)

        usuario = usuario[start:start + length]

    data = [{'id': usu.id,'nombre': usu.first_name, 
            'apellido': usu.last_name, 'email': usu.email,
            'username': usu.username} for usu in usuario]        
        
    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

@login_required()
@permission_required('usuario.view_user')
def list_usuarios_baja(request):    
    return render(request, "usuario/list_usuarios_baja.html")


@login_required()
def list_usuarios_baja_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        usuario = User.objects.exclude(is_active=True).filter(Q(first_name__icontains=query) 
        | Q(last_name__icontains=query) | Q(username__icontains=query))
        usuario = usuario.exclude(is_superuser=True)
    else:
        usuario = User.objects.exclude(is_active=True).all()
        usuario = usuario.exclude(is_superuser=True)


    total = usuario.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
     
        usuario = usuario[start:start + length]

    data = [{'id': usu.id,'nombre': usu.first_name, 'apellido': usu.last_name, 
    'email': usu.email, 'username': usu.username} for usu in usuario]        
            
    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

@login_required()
@permission_required('usuario.add_user')
def add_usuario(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Se ha agregado correctamente!")
            return redirect('/usuario/listUsuarios/')
    context = {'form': form}
    return render(request, 'usuario/add_usuario.html', context)

@login_required()
@permission_required('usuario.change_user')
def edit_usuario(request, id):
    try:
        usuario = User.objects.get(id=id)
        form = UserFormChange(request.user, instance=usuario)
        if request.method == 'POST':
            form = UserFormChange(request.user, request.POST, instance=usuario)
            if not form.has_changed():
                messages.info(request, "No ha hecho ningun cambio")
                return redirect('/usuario/edit/' + str(id))
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                messages.add_message(request, messages.SUCCESS, 'Se ha editado correctamente!')
                return redirect('/usuario/edit/' + str(id))
        context = {'form': form, 'usuario': usuario}
        return render(request, 'usuario/edit_usuario.html', context)
    except Exception as e:
            messages.add_message(request, messages.SUCCESS, 'ha ocurrido un error, intentelo mas tarde!')
            return redirect('/usuario/listUsuarios/')


@login_required()
@permission_required('usuario.delete_user')
def baja_usuario(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        if request.user == user:
            messages.error(request, "¡No puedes eliminar este usuario! intentelo mas tarde.")
            confirm = False
            return redirect('/usuario/listUsuarios/')
        else:
            user.is_active = False
            user.save()
            messages.error(request, "Se ha dado de baja correctamente!.")    
            return redirect('/usuario/listUsuarios/')

    context = {"user": user}
    return render(request, 'usuario/dar_baja_usuario_modal.html', context)

@login_required()
@permission_required('usuario.add_user')
def alta_usuario(request, id):
    user = User.objects.get(id=id)
    if request.user == user:
        messages.error(request, "¡No puedes eliminar este usuario! intentelo mas tarde.")
        return redirect('/usuario/listUsuariosBaja/')
    else:
        user.is_active = True
        user.save()
        messages.error(request, "Se ha dado de alta correctamente!.")    
        return redirect('/usuario/listUsuariosBaja/')


@login_required()
@permission_required('usuario.change_user')
def change_password(request, id):
    form = ContraseñaChangeForm(request.user)
    if request.method == 'POST':
        form = ContraseñaChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.SUCCESS, 'Se ha editado correctamente!')
            return redirect('/usuario/editPassword/' + str(id))
    
    context = {'form': form, 'id': id}
    return render(request, 'usuario/edit_password.html', context)

#Roles
def get_group_list(request):
    query = request.GET.get('busqueda')
    if query != "":
        group = Group.objects.filter(Q(name__icontains=query))
    else:
        group = Group.objects.all()

    total = group.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        group = group[start:start + length]

    data = [{'id': g.id,'rol': g.name} for g in group]        
        
    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

@login_required()
@permission_required('usuario.add_user')
def add_rol(request):
    form = GroupForm()
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Se ha agregado correctamente!")
            return redirect('/usuario/addRol/')
        else:
            messages.error(request, form.errors)

    context = {'form': form,'groups': Group.objects.all()}
    return render(request, 'usuario/add_rol.html', context)

@login_required()
@permission_required('usuario.add_user')
def edit_rol(request, id):
    group = Group.objects.get(id=id)
    form = GroupChangeForm(instance=group)
    if request.method == 'POST':
        form = GroupChangeForm(request.POST, instance=group)
        if not form.has_changed():
            messages.info(request, "No ha hecho ningun cambio")
            return redirect('/usuario/addRol/')
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Se ha editado correctamente!')
            return redirect('/usuario/addRol/')
        else:
            messages.error(request, form.errors)

    context = {'form': form,'groups': Group.objects.all()}

    return render(request, 'usuario/add_rol.html', context)

@login_required()
@permission_required('usuario.delete_user')
def delete_rol(request, id):
    group = Group.objects.get(id=id)
    group.delete()
    return redirect('/usuario/addRol/')

