# Generated by Django 4.1.7 on 2023-06-01 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0002_facturacompra_pago_pedido_pedidocabecera_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facturacompra',
            name='fecha_alta',
            field=models.CharField(default='31/05/2023', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='fecha_alta',
            field=models.CharField(default='31/05/2023 22:37:19 hs', editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='pedidocabecera',
            name='fecha_alta',
            field=models.CharField(default='31/05/2023', editable=False, max_length=200),
        ),
    ]
