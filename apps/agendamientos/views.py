from django.shortcuts import render

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import time, datetime, date
import json

from apps.agendamientos.forms import ReservaForm
from apps.agendamientos.models import Reserva
from apps.configuracion.empleado.models import Empleado
from apps.configuracion.servicio.models import Servicio
from apps.mascotas.models import Mascota

hora_entrada = "08:00"
hora_salida_lun_vie = "18:00"
hora_salida_sab = "15:00"
today = date.today()
#Reservas
@login_required()
@permission_required('reserva.add_reserva')
def add_reserva(request):
    form = ReservaForm
    servicios = Servicio.objects.exclude(is_active="N").order_by('-last_modified')
    if request.method == 'POST':
        form = ReservaForm(request.POST) 
        if form.is_valid():           
            form.save()            
            messages.success(request, 'Se ha agregado correctamente!')
            try:
                emp = Empleado.objects.get(id=request.POST.get('id_empleado'))
                emp.emp_disponible_reserva = 'N'
                emp.save()
                masc = Mascota.objects.get(id=request.POST.get('id_mascota'))
                masc.masc_reservado = 'N'
                masc.fecha_reservada = request.POST.get('fecha_reserva')
                masc.hora_reserva = request.POST.get('hora_reserva')
                masc.save()
            except Exception as e:
                pass
            return redirect('/reserva/listReserva/')
    context = {'form' : form}
    return render(request, 'reserva/add_reserva_modal.html', context)

@login_required()
@permission_required('reserva.change_reserva')
def edit_reserva(request, id):
    reserva = Reserva.objects.get(id=id)
    form = ReservaForm(instance=reserva)
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if not form.has_changed():
            messages.info(request, "No has hecho ningun cambio!")
            return redirect('/reserva/listReserva/')
        if form.is_valid():
            reserva = form.save(commit=False)
            emp = Empleado.objects.get(id=request.POST.get('id_empleado'))
            masc = Mascota.objects.get(id=request.POST.get('id_mascota'))
            estado = request.POST.get('estado_re')
            if estado == 'FIN' or estado == 'CAN':
                reserva.disponible_emp = "S"
                emp.emp_disponible_reserva = 'S' 
                masc.masc_reservado = 'S'
                masc.fecha_reservada = ""
                masc.hora_reserva = ""                                                    
            reserva.save()
            emp.save()
            masc.save()
            messages.success(request, 'Se ha editado correctamente!')
            return redirect('/reserva/listReserva/')
    context = {'form' : form, 'reserva': reserva}
    return render(request, 'reserva/edit_reserva_modal.html', context)

@login_required()
@permission_required('reserva.view_reserva')
def list_reserva(request):
    data = []
    reserva = Reserva.objects.all()
    fechaDate = date(today.year, today.month, today.day)
    for r in reserva:
        if r.fecha_reserva is not None:
            if fechaDate > r.fecha_reserva:
                if r.estado_re == 'PEN':
                    r.estado_re = 'FIN'
                    r.disponible_emp = "S"
                    r.color_estado = "green"
                    try:
                        masc = Mascota.objects.get(id=r.id_mascota.id)
                        masc.masc_reservado = "S"
                        masc.fecha_reservada = ""
                        masc.hora_reserva = ""
                        masc.save()
                    except:
                        pass
                    r.save()                                                     
    paginator = Paginator(reserva, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj' : page_obj}
    return render(request, "reserva/list_reserva.html", context)

#Metodo para eliminar servicio
@login_required()
@permission_required('reserva.delete_reserva')
def delete_reserva(request, id):
    reserva = Reserva.objects.get(id=id)
    reserva.delete()
    messages.success(request, 'La reserva se ha eliminado!')
    return redirect('/reserva/listReserva/')

@login_required()
def search_reserva(request):
    query = request.GET.get('q')
    if query:
        reserva = Reserva.objects.exclude(is_active="N").filter(Q(fecha_reserva__icontains=query))
    else:
        reserva = Reserva.objects.exclude(is_active="N").order_by('-last_modified')
    paginator = Paginator(reserva, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = { 'page_obj': page_obj}
    return render(request, "reserva/list_reserva.html", context)
        

def validar_fecha_hora(request):
    fecha = request.GET.get('fecha')
    hora = request.GET.get('hora')
    horaSelected = hora.split(':')
    servicio = request.GET.get('servicio')
    cliente = request.GET.get('id_cliente')
    mascota = request.GET.get('id_mascota')
    emp = request.GET.get('empleado')
    action = request.GET.get('action')
    id_reserva_r = request.GET.get('id_reserva')
    diaActual = datetime.now()
    mesActual =  str(diaActual.month) if diaActual.month > 9 else '0' + str(diaActual.month)
    dayActual = str(diaActual.day) if diaActual.day > 9 else '0' + str(diaActual.day)
    diaCompare = str(diaActual.year) + "-" + mesActual + "-" + dayActual
    messageReponse = ""
    isFalse = True
    isFalseOtherDay = True
    isFalseMascota = True   
    isFalseEmpleado = True
    splitHoraActual = diaActual.hour
    empe_dispo = Empleado.objects.get(id=emp)
    serviEmpleado = Empleado.objects.filter(id_servicio=servicio).exclude(disponible=False)
    countEmpleadoServi = Empleado.objects.filter(id_servicio=servicio).exclude(disponible=False).count()
    countEmpleadoDiaServi = Reserva.objects.filter(id_servicio=servicio, fecha_reserva=fecha, hora_reserva=hora).exclude(disponible_emp='S').count()
    mas_disponible = Mascota.objects.get(id=mascota)
    try:        
        reserva_compare = Reserva.objects.get(id=id_reserva_r)
    except:
        pass

    if diaCompare == fecha:
        if splitHoraActual <= int(horaSelected[0]):
            if action == 'A':
                if countEmpleadoServi <= countEmpleadoDiaServi: 
                    messageReponse = "Ya no hay disponibilidad del servicio para esa hora"
                    response = { 'mensaje': messageReponse}
                    return JsonResponse(response)
                else:
                    try:
                        reserva = Reserva.objects.get(fecha_reserva=fecha, hora_reserva=hora, id_empleado=emp, id_servicio=servicio)
                        if empe_dispo.emp_disponible_reserva == 'S':
                            isFalseEmpleado = False
                    except Exception as e:
                        if empe_dispo.emp_disponible_reserva == 'S':
                            isFalseEmpleado = False                    
                        else:
                            isFalseEmpleado = True                    
                        reserva = Reserva.objects.filter(fecha_reserva=fecha, hora_reserva=hora, id_empleado=emp, id_servicio=servicio)
                        if reserva.count() > 0:
                            for r in reserva:
                                if r.estado_re == 'PEN':
                                    isFalseEmpleado = True
                        else: 
                            isFalseEmpleado = False
                    if isFalseEmpleado:
                        messageReponse = "El empleado ya esta asignado a un trabajo para esa hora y dia"
                        response = { 'mensaje': messageReponse}
                        return JsonResponse(response) 

                    try: 
                        reserva = Reserva.objects.get(fecha_reserva=fecha, hora_reserva=hora, id_mascota=mascota, id_cliente=cliente)
                        if mas_disponible.masc_reservado == 'S':
                                isFalseMascota = False
                    except:                    
                        if mas_disponible.masc_reservado == 'S':
                            isFalseMascota = False
                        else:
                            isFalseMascota = True
                        reserva = Reserva.objects.filter(fecha_reserva=fecha, hora_reserva=hora, id_mascota=mascota, id_cliente=cliente)
                        if reserva.count() > 0:
                            for r in reserva:
                                if r.estado_re == 'PEN':
                                    isFalseMascota = True
                        else: 
                            if mas_disponible.masc_reservado == 'S':
                                isFalseMascota = False
                            else:
                                isFalseMascota = True
                        
                    if isFalseMascota:                    
                        messageReponse = "Esta mascota ya tiene una reserva para este dia y hora"
                        response = { 'mensaje': messageReponse}
                        return JsonResponse(response)
                    try:
                        reserva = Reserva.objects.get(fecha_reserva=fecha, id_servicio=servicio, id_cliente=cliente, hora_reserva=hora, id_mascota=mascota, id_empleado=emp)
                    except:
                        isFalse = False
                    if isFalse:
                        messageReponse = "Este cliente ya tiene una reserva para ese dia y hora"
                        response = { 'mensaje': messageReponse}
                        return JsonResponse(response) 
            else:
                if (int(reserva_compare.id_empleado.id) != int(emp) or int(reserva_compare.id_servicio.id) != int(servicio) and 
                    reserva_compare.hora_reserva != hora):
                    try:                            
                        reserva = Reserva.objects.get(fecha_reserva=fecha, hora_reserva=hora, id_empleado=emp, id_servicio=servicio)            
                        if empe_dispo.emp_disponible_reserva == 'S':
                            isFalseEmpleado = False
                    except Exception as e:
                        if empe_dispo.emp_disponible_reserva == 'S':
                            isFalseEmpleado = False                    
                        else:
                            isFalseEmpleado = True                    
                        reserva = Reserva.objects.filter(fecha_reserva=fecha, hora_reserva=hora, id_empleado=emp, id_servicio=servicio)
                        if reserva.count() > 0:
                            for r in reserva:
                                if r.estado_re == 'PEN':
                                    isFalseEmpleado = True
                        else: 
                            isFalseEmpleado = False
                    if isFalseEmpleado:
                        messageReponse = "El empleado ya esta asignado a un trabajo para esa hora y dia"
                        response = { 'mensaje': messageReponse}
                        return JsonResponse(response)
                if (int(reserva_compare.id_servicio.id) != int(servicio)):
                    if(int(reserva_compare.id_cliente.id) != int(cliente) or int(reserva_compare.id_mascota.id != int(mascota))):
                        try:
                            reserva = Reserva.objects.get(fecha_reserva=fecha, hora_reserva=hora, id_mascota=mascota, id_cliente=cliente, id_servicio=servicio)
                            if mas_disponible.masc_reservado == 'S':
                                isFalseMascota = False
                        except:                    
                            if mas_disponible.masc_reservado == 'S':
                                isFalseMascota = False
                            else:
                                isFalseMascota = True
                            reserva = Reserva.objects.filter(fecha_reserva=fecha, hora_reserva=hora, id_mascota=mascota, id_cliente=cliente, id_servicio=servicio)
                            if reserva.count() > 0:
                                for r in reserva:
                                    if r.estado_re == 'PEN':
                                        isFalseMascota = True
                            else: 
                                if mas_disponible.masc_reservado == 'S':
                                    isFalseMascota = False
                                else:
                                    isFalseMascota = True                            
                        if isFalseMascota:
                            messageReponse = "Esta mascota ya tiene una reserva para este dia y hora"
                            response = { 'mensaje': messageReponse}
                            return JsonResponse(response)
                        try:
                            reserva = Reserva.objects.get(fecha_reserva=fecha, id_cliente=cliente, hora_reserva=hora, id_mascota=mascota)
                        except:
                            isFalse = False
                        if isFalse:
                            messageReponse = "Este cliente ya tiene una reserva para ese dia y hora"
                            response = { 'mensaje': messageReponse}
                            return JsonResponse(response)
                if(int(reserva_compare.id_cliente.id) != int(cliente) and int(reserva_compare.id_mascota.id != int(mascota))):
                    try:
                        reserva = Reserva.objects.get(fecha_reserva=fecha, hora_reserva=hora, id_mascota=mascota, id_cliente=cliente)
                        if mas_disponible.masc_reservado == 'S':
                                isFalseMascota = False
                    except:                    
                        if mas_disponible.masc_reservado == 'S':
                            isFalseMascota = False
                        else:
                            isFalseMascota = True
                        reserva = Reserva.objects.filter(fecha_reserva=fecha, hora_reserva=hora, id_mascota=mascota, id_cliente=cliente)
                        if reserva.count() > 0:
                            for r in reserva:
                                if r.estado_re == 'PEN':
                                    isFalseMascota = True
                        else: 
                            if mas_disponible.masc_reservado == 'S':
                                isFalseMascota = False
                            else:
                                isFalseMascota = True
                        
                    if isFalseMascota:
                        messageReponse = "Esta mascota ya tiene una reserva para este dia y hora"
                        response = { 'mensaje': messageReponse}
                        return JsonResponse(response)
                    try:
                        reserva = Reserva.objects.get(fecha_reserva=fecha, id_cliente=cliente, hora_reserva=hora, id_mascota=mascota, id_servicio=servicio)
                    except:
                        isFalse = False
                    if isFalse:
                        messageReponse = "Este cliente ya tiene una reserva para ese dia y hora"
                        response = { 'mensaje': messageReponse}
                        return JsonResponse(response)
        else:
            messageReponse = "Has seleccionado un horario que ya a ha pasado"
            response = { 'mensaje': messageReponse}
            return JsonResponse(response)
    else:
        if action == 'A':
            if countEmpleadoServi <= countEmpleadoDiaServi:
                messageReponse = "Ya no hay disponibilidad del servicio para esa hora y dia"
                response = { 'mensaje': messageReponse}
                return JsonResponse(response)
            else:
                try:                
                    reserva = Reserva.objects.get(fecha_reserva=fecha, hora_reserva=hora, id_empleado=emp, id_servicio=servicio)
                    if empe_dispo.emp_disponible_reserva == 'S':
                        isFalseEmpleado = False
                except Exception as e:
                    if empe_dispo.emp_disponible_reserva == 'S':
                        isFalseEmpleado = False                    
                    else:
                        isFalseEmpleado = True                    
                    reserva = Reserva.objects.filter(fecha_reserva=fecha, hora_reserva=hora, id_empleado=emp, id_servicio=servicio)
                    if reserva.count() > 0:
                        for r in reserva:
                            if r.estado_re == 'PEN':
                                isFalseEmpleado = True
                    else: 
                        isFalseEmpleado = False
                if isFalseEmpleado:
                    messageReponse = "El empleado ya esta asignado a un trabajo para esa hora y dia"
                    response = { 'mensaje': messageReponse}
                    return JsonResponse(response)            
                try: 
                    reserva = Reserva.objects.get(fecha_reserva=fecha, hora_reserva=hora, id_mascota=mascota, id_cliente=cliente)
                    if mas_disponible.masc_reservado == 'S':
                            isFalseMascota = False
                except Exception as e:                    
                    reserva = Reserva.objects.filter(fecha_reserva=fecha, hora_reserva=hora, id_mascota=mascota, id_cliente=cliente)
                    if reserva.count() > 0:
                        for r in reserva:
                            if r.estado_re == 'PEN':
                                isFalseMascota = True
                    else: 
                        if mas_disponible.masc_reservado == 'S':
                            isFalseMascota = False
                        else:
                            if mas_disponible.fecha_reservada == fecha and mas_disponible.hora_reserva == hora:
                                isFalseMascota = True
                            else: 
                                isFalseMascota = False
                if isFalseMascota:
                    messageReponse = "Esta mascota ya tiene una reserva para este dia y hora"
                    response = { 'mensaje': messageReponse}
                    return JsonResponse(response)
                try:
                    reserva = Reserva.objects.get(fecha_reserva=fecha, id_servicio=servicio, id_cliente=cliente, hora_reserva=hora, id_mascota=mascota, id_empleado=emp)        
                except:
                    isFalse = False
                if isFalse:
                    messageReponse = "Este cliente ya tiene una reserva para ese dia y hora"
                    response = { 'mensaje': messageReponse}
                    return JsonResponse(response)
        else:
            if (int(reserva_compare.id_empleado.id) != int(emp) or int(reserva_compare.id_servicio.id) != int(servicio) and 
                    reserva_compare.hora_reserva != hora):
                try:                            
                    reserva = Reserva.objects.get(fecha_reserva=fecha, hora_reserva=hora, id_empleado=emp, id_servicio=servicio)            
                    if empe_dispo.emp_disponible_reserva == 'S':
                        isFalseEmpleado = False
                except Exception as e:
                    if empe_dispo.emp_disponible_reserva == 'S':
                        isFalseEmpleado = False                    
                    else:
                        isFalseEmpleado = True                    
                    reserva = Reserva.objects.filter(fecha_reserva=fecha, hora_reserva=hora, id_empleado=emp, id_servicio=servicio)
                    if reserva.count() > 0:
                        for r in reserva:
                            if r.estado_re == 'PEN':
                                isFalseEmpleado = True
                    else: 
                        isFalseEmpleado = False
                if isFalseEmpleado:
                    messageReponse = "El empleado ya esta asignado a un trabajo para esa hora y dia"
                    response = { 'mensaje': messageReponse}
                    return JsonResponse(response)
            if (int(reserva_compare.id_servicio.id) != int(servicio)):
                if(int(reserva_compare.id_cliente.id) != int(cliente) or int(reserva_compare.id_mascota.id != int(mascota))):
                    try:
                        reserva = Reserva.objects.get(fecha_reserva=fecha, hora_reserva=hora, id_mascota=mascota, id_cliente=cliente, id_servicio=servicio)
                        if mas_disponible.masc_reservado == 'S':
                                isFalseMascota = False
                    except:                    
                        reserva = Reserva.objects.filter(fecha_reserva=fecha, hora_reserva=hora, id_mascota=mascota, id_cliente=cliente)
                        if reserva.count() > 0:
                            for r in reserva:
                                if r.estado_re == 'PEN':
                                    isFalseMascota = True
                        else: 
                            if mas_disponible.masc_reservado == 'S':
                                isFalseMascota = False
                            else:
                                if mas_disponible.fecha_reservada == fecha and mas_disponible.hora_reserva == hora:
                                    isFalseMascota = True
                                else: 
                                    isFalseMascota = False                   
                    if isFalseMascota:
                        messageReponse = "Esta mascota ya tiene una reserva para este dia y hora"
                        response = { 'mensaje': messageReponse}
                        return JsonResponse(response)
                    try:
                        reserva = Reserva.objects.get(fecha_reserva=fecha, id_cliente=cliente, hora_reserva=hora, id_mascota=mascota)
                    except:
                        isFalse = False
                    if isFalse:
                        messageReponse = "Este cliente ya tiene una reserva para ese dia y hora"
                        response = { 'mensaje': messageReponse}
                        return JsonResponse(response)
            if(int(reserva_compare.id_cliente.id) != int(cliente) and int(reserva_compare.id_mascota.id != int(mascota))):
                try:
                    reserva = Reserva.objects.get(fecha_reserva=fecha, hora_reserva=hora, id_mascota=mascota, id_cliente=cliente)
                    if mas_disponible.masc_reservado == 'S':
                            isFalseMascota = False
                except:                    
                    reserva = Reserva.objects.filter(fecha_reserva=fecha, hora_reserva=hora, id_mascota=mascota, id_cliente=cliente)
                    if reserva.count() > 0:
                        for r in reserva:
                            if r.estado_re == 'PEN':
                                isFalseMascota = True
                    else: 
                        if mas_disponible.masc_reservado == 'S':
                            isFalseMascota = False
                        else:
                            if mas_disponible.fecha_reservada == fecha and mas_disponible.hora_reserva == hora:
                                isFalseMascota = True
                            else: 
                                isFalseMascota = False
                    
                if isFalseMascota:
                    messageReponse = "Esta mascota ya tiene una reserva para este dia y hora"
                    response = { 'mensaje': messageReponse}
                    return JsonResponse(response)
                try:
                    reserva = Reserva.objects.get(fecha_reserva=fecha, id_cliente=cliente, hora_reserva=hora, id_mascota=mascota, id_servicio=servicio)
                except:
                    isFalse = False
                if isFalse:
                    messageReponse = "Este cliente ya tiene una reserva para ese dia y hora"
                    response = { 'mensaje': messageReponse}
                    return JsonResponse(response)
    response = { 'mensaje': messageReponse}
    return JsonResponse(response)


def get_mascota_cliente(request):
    cliente = request.GET.get('id_cliente')

    mascotas = Mascota.objects.filter(id_cliente=cliente)

    listMascota = [{'id': mascota.id, 'nombre': mascota.nombre_mascota} for mascota in mascotas]

    listJsonMascotas = json.dumps(listMascota)
    if listJsonMascotas != '[]':
        response = { 'mascota': listJsonMascotas, 'mensaje': "Ok"}
        return JsonResponse(response)
    response = { 'mascota': listJsonMascotas, 'mensaje': ""}       
    return JsonResponse(response)

def get_min_service(request):
    servicio = request.GET.get('servicio')
    emp = Empleado.objects.filter(id_servicio=servicio)
    listEmpleado = [{'id': empleado.id, 'nombre': empleado.nombre_emp + " " + empleado.apellido_emp} for empleado in emp]

    listJsonEmpleado= json.dumps(listEmpleado)
    isFalse = True
    try:
        minService = Servicio.objects.get(id=servicio)
    except:
        isFalse = False
    if isFalse:
        response = { 'tiempo': minService.min_serv, 'mensaje': "Ok", 'empleado': listJsonEmpleado}
        return JsonResponse(response)
    response = { 'tiempo': minService.min_serv, 'mensaje': "", 'empleado': listJsonEmpleado}       
    return JsonResponse(response)

def get_mascota_selected(request):
    id_reserva = request.GET.get('id_reserva')
    cliente = request.GET.get('id_cliente')
    hora_reserva = request.GET.get('hora_reserva')
    fecha_reserva = request.GET.get('fecha_reserva')
    servicio = request.GET.get('servicio')
    emp = Empleado.objects.filter(id_servicio=servicio)
    mascotas = Mascota.objects.filter(id_cliente=cliente)
    listMascota = [{'id': mascota.id, 'nombre': mascota.nombre_mascota} for mascota in mascotas]
    listEmpleado = [{'id': empleado.id, 'nombre': empleado.nombre_emp + " " + empleado.apellido_emp} for empleado in emp]

    listJsonEmpleado= json.dumps(listEmpleado)
    listJsonMascotas = json.dumps(listMascota)
    reserva = Reserva.objects.get(id=id_reserva, fecha_reserva=fecha_reserva, id_servicio=servicio, id_cliente=cliente, hora_reserva=hora_reserva)
    if listJsonMascotas != '[]':
        response = { 'mascota': listJsonMascotas, 'mensaje': "Ok", 'mascota_selected': reserva.id_mascota.id, 'empleado': reserva.id_empleado.id, 'empleados':listJsonEmpleado}
        return JsonResponse(response)
    response = { 'mascota': listJsonMascotas, 'mensaje': ""}       
    return JsonResponse(response)


