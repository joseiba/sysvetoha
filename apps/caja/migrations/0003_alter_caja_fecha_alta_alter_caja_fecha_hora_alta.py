# Generated by Django 4.1.7 on 2023-06-24 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caja', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caja',
            name='fecha_alta',
            field=models.CharField(default='24/06/2023', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='caja',
            name='fecha_hora_alta',
            field=models.CharField(default='24/06/2023 12:27:51 hs', max_length=500, null=True),
        ),
    ]