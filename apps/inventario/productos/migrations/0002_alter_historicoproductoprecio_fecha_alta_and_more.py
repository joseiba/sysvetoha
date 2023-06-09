# Generated by Django 4.1.7 on 2023-06-24 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicoproductoprecio',
            name='fecha_alta',
            field=models.CharField(default='24/06/2023', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='inventario',
            name='fecha_alta',
            field=models.CharField(default='24/06/2023 12:27:51 hs', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='fecha_compra',
            field=models.CharField(default='24/06/2023', editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='tipoproducto',
            name='fecha_alta',
            field=models.CharField(default='24/06/2023 12:27:51 hs', editable=False, max_length=200),
        ),
    ]
