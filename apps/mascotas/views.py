from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import date, datetime
import json
import math

from .models import Especie, Mascota, Raza
from .forms import EspecieForm, MascotaForm, RazaForm

# Create your views here.

#@permission_required('mascota.add_especie')
def add_especie(request):
    form = EspecieForm
    if request.method == 'POST':
        form = EspecieForm(request.POST or None)
        if form.is_valid():
            messages.success(request, 'Se ha agregado correctamente!')
            form.save()
            return redirect('/mascota/listEspecie/')
    context = {'form' : form}
    return render(request, 'mascota/especie/add_especie_modal.html', context)


#@login_required()
#@permission_required('mascota.change_especie')
def edit_especie(request, id):
    especie = Especie.objects.get(id=id)
    form = EspecieForm(instance=especie)
    if request.method == 'POST':
        form = EspecieForm(request.POST, instance=especie)
        if not form.has_changed():
            messages.info(request, "No has hecho ningun cambio!")
            return redirect('/mascota/listEspecie/')
        if form.is_valid():
            especie = form.save(commit=False)
            especie.save()
            messages.success(request, 'Se ha editado correctamente!')
            return redirect('/mascota/listEspecie/')
    context = {'form' : form, 'especie': especie}
    return render(request, 'mascota/especie/add_especie_modal.html', context)

#@login_required()
#@permission_required('mascota.view_especie')
def list_especie(request):
    especie = Especie.objects.all().order_by('-last_modified')
    paginator = Paginator(especie, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj' : page_obj}
    return render(request, "mascota/especie/list_especie.html", context)

#@login_required()
def list_especie_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        especie = Especie.objects.filter(Q(nombre_especie__icontains=query))
    else:
        especie = Especie.objects.all().order_by('-last_modified')

    total = especie.count()


    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        especie = especie[start:start + length]

    data = [{'id': espe.id, 'nombre': espe.nombre_especie} for espe in especie]        

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)    

#@login_required()
def search_especie(request):
    query = request.GET.get('q')
    if query:
        especie = Especie.objects.filter(Q(nombre_especie__icontains=query))
    else:
        especie = Especie.objects.all().order_by('-last_modified')
    paginator = Paginator(especie, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = { 'page_obj': page_obj}
    return render(request, "mascota/especie/list_especie.html", context)

    """
    Functions of Razas
    """
#@login_required()
#@permission_required('mascota.add_raza')
def add_raza(request):
    form = RazaForm
    if request.method == 'POST':
        form = RazaForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha agregado correctamente!')
            return redirect('/mascota/listRaza/')
    context = {'form' : form}
    return render(request, 'mascota/raza/add_raza_modal.html', context)

#@login_required()
#@permission_required('mascota.change_raza')
def edit_raza(request, id):
    raza = Raza.objects.get(id=id)
    form = RazaForm(instance=raza)
    if request.method == 'POST':
        form = RazaForm(request.POST, instance=raza)
        if not form.has_changed():
            messages.info(request, "No has hecho ningun cambio!")
            return redirect('/mascota/listRaza/')
        if form.is_valid():
            raza = form.save(commit=False)
            raza.save()
            messages.success(request, 'Se ha editado correctamente!')
            return redirect('/mascota/listRaza/')
    context = {'form' : form, 'raza': raza}
    return render(request, 'mascota/raza/add_raza_modal.html', context)    

#@login_required()
#@permission_required('mascota.view_raza')
def list_raza(request):
    raza = Raza.objects.all().order_by('-last_modified')
    raza_especie = RazaForm
    paginator = Paginator(raza, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj' : page_obj, 'form': raza_especie}
    return render(request, "mascota/raza/list_raza.html", context)

#@login_required()
def get_list_raza_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        raza = Raza.objects.filter(Q(nombre_raza__icontains=query) | Q(id_especie__nombre_especie__icontains=query) )
    else:
        raza = Raza.objects.all().order_by('-last_modified')

    total = raza.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        raza = raza[start:start + length]

    data = [{'id': ra.id, 'nombre_raza': ra.nombre_raza, 'nombre_especie': ra.id_especie.nombre_especie } for ra in raza]        

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response) 

#@login_required()
def search_raza(request):
    query = request.GET.get('q')
    if query:
        raza = Raza.objects.filter(Q(nombre_raza__icontains=query))
    else:
        raza = Raza.objects.all().order_by('-last_modified')
    paginator = Paginator(raza, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = { 'page_obj': page_obj}
    return render(request, "mascota/raza/list_raza.html", context)


@login_required()
@permission_required('mascota.view_mascota')
def list_mascotas(request):
    mascotas = Mascota.objects.all().order_by('-last_modified')
    paginator = Paginator(mascotas, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj' : page_obj}
    return render(request, "mascota/mascota/list_mascota.html", context)


date = datetime.now()
# Create your views here.
@login_required()
@permission_required('mascota.add_mascota')
def add_mascota(request):
    form = MascotaForm    
    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES)
        if form.is_valid():           
            form.save()
            messages.success(request, 'Se ha agregado correctamente!')
            return redirect('/mascota/add')
    context = {'form' : form}
    return render(request, 'mascota/mascota/add_mascota.html', context)


@login_required()
@permission_required('mascota.view_mascota')
def edit_mascota(request, id):
    mascota = Mascota.objects.get(id=id)
    form = MascotaForm(instance=mascota)
    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES, instance=mascota)
        if not form.has_changed():
            messages.info(request, "No has hecho ningun cambio!")
            return redirect('/mascota/edit/' + str(id))
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.save()
            messages.success(request, 'Se ha editado correctamente!')
            return redirect('/mascota/edit/' + str(id))

    context = {'form': form, 'mascota': mascota}
    return render(request, 'mascota/mascota/edit_mascota.html', context)