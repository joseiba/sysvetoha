from django.db import models
from datetime import date, datetime
from apps.cliente.models import Cliente

from vetoho.settings import MEDIA_URL, STATIC_URL

url_pets_image = 'base/img/test.jfif'

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
        
class Mascota(models.Model):
    """[summary]

    Args:
        models ([Mascota]): [Contiene la informacion de las mascotas]
    """    
    nombre_mascota = models.CharField(max_length=200, help_text="Ingrese nombre de la mascota")
    tatuaje = models.CharField(max_length=200, default="-", null=True, blank=True,  help_text="Ingrese el tatuaje")
    MACHO = 'MAC'
    HEMBRA = 'HEB'    
    tipo_sexo =((MACHO, 'Macho'),
                (HEMBRA, 'Hembra'))

    sexo = models.CharField(max_length=15, choices=tipo_sexo, default="-", help_text="Seleccione el sexo")
    edad = models.CharField(max_length = 200, default = '-', null = True, blank = True)
    imagen = models.ImageField(upload_to='mascotas/fotos', null=True, blank=True, help_text="Ingrese una foto")
    peso = models.CharField(max_length = 200, help_text="Ingrese el peso de la mascota")
    fecha_nacimiento =  models.DateField(null = True, blank = True)
    masc_reservado = models.CharField(max_length=200, blank=True, null=True, default="S")
    fecha_reservada = models.CharField(max_length=200, blank=True, null=True)
    hora_reserva = models.CharField(max_length=200, blank=True, null=True)
    color_pelaje = models.CharField(max_length=200, default = '-', null = True, blank = True, help_text="Ingrese el color de la mascota")
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    id_raza = models.ForeignKey('Raza', on_delete=models.CASCADE, null=False)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = "Mascota"
        verbose_name_plural = "Mascotas"
        default_permissions =  ()
        permissions = (
                ('add_mascota', 'Agregar Mascota'),
                ('change_mascota', 'Editar Mascota'),
                ('delete_mascota', 'Eliminar Mascota'),
                ('view_mascota', 'Listar Mascotas'))  

    '''def save(self, *args, **kwargs):
        # Opening the uploaded image
        img = Image.open(self.imagen)
        if :
            super().save(*args, **kwargs)

        if img.height > 200 or img.width > 200:

            output_size = (200, 200)
            img.thumbnail(output_size)
            img = img.convert('RGB')

            output = BytesIO()
            img.save(output, format='JPEG')
            output.seek(0)

            # change the imagefield value to be the newley modifed image value
            self.imagen = InMemoryUploadedFile(output, 'ImageField',
                                            f'{self.imagen.name.split(".")[0]}.jpg',
                                            'image/jpeg', sys.getsizeof(output),
                                            None)

        super().save(*args, **kwargs)'''
    def __str__(self):
        return self.nombre_mascota

    def get_profile(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, url_pets_image)
    
    def save(self, *args, **kwargs):
        is_new = not self.id
        super().save(*args, **kwargs)
        # if is_new:
        #     FichaMedica.objects.create(id_mascota=self)        