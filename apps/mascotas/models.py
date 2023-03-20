from django.db import models
from datetime import date, datetime

# Create your models here.
date = datetime.now()

class Especie(models.Model):      
    nombre_especie = models.CharField(max_length=200, help_text = "Ingrese el nombre de la Especie")
    last_modified = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        verbose_name = "Especie"
        verbose_name_plural = "Especies"
        default_permissions =  ()
        permissions = (
            ('add_especie', 'Agregar Especie'),
            ('change_especie', 'Editar Especie'),
            ('delete_especie', 'Eliminar Especie'),
            ('view_especie', 'Listar Especies'))         

    def __str__(self):
        return self.nombre_especie

class Raza(models.Model):      
    nombre_raza = models.CharField(max_length=200, help_text = "Ingrese el nombre de la Raza")
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    id_especie = models.ForeignKey('Especie', on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = "Raza"
        verbose_name_plural = "Razas"
        default_permissions =  ()
        permissions = (
            ('add_raza', 'Agregar Raza'),
            ('change_raza', 'Editar Raza'),
            ('delete_raza', 'Eliminar Raza'),
            ('view_raza', 'Listar Razas'))   

        def __str__(self):
            return self.nombre_raza  