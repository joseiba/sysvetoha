from django.contrib.auth.models import AbstractUser
from django.db import models
from config.settings import STATIC_URL, MEDIA_URL


class User(AbstractUser):
    profile = models.ImageField(upload_to='user/fotos', null=True, blank=True)

    def get_profile(self):
        if self.profile:
            return '{}{}'.format(MEDIA_URL, self.profile)
        return '{}{}'.format(STATIC_URL, 'img/profile.png')

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        default_permissions =  ()
        permissions = (
            ('add_user', 'Agregar Usuario'),
            ('change_user', 'Editar Usuario'),
            ('delete_user', 'Eliminar Usuario'),
            ('view_user', 'Listar Usuarios'))       
