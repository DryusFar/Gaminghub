# Generated by Django 4.0.4 on 2023-05-10 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gaminghub', '0003_perfilusuario_edad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicacion',
            name='multimedia',
            field=models.ImageField(null=True, upload_to='media/'),
        ),
    ]
