# Generated by Django 4.2 on 2023-05-10 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gaminghub', '0002_remove_perfilusuario_nombre_completo'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfilusuario',
            name='edad',
            field=models.IntegerField(default=12),
            preserve_default=False,
        ),
    ]
