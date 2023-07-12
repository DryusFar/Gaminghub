# Generated by Django 4.2 on 2023-07-11 23:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Amistad',
            fields=[
                ('id_amistad', models.BigAutoField(primary_key=True, serialize=False)),
                ('persona', models.IntegerField(null=True)),
                ('amigo', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id_grupo', models.BigAutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=300)),
                ('multimedia', models.ImageField(default='static/img/Logo.png', max_length=200, upload_to='')),
                ('privacidad', models.IntegerField()),
                ('fk_id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RolUsuario',
            fields=[
                ('id_rol', models.BigAutoField(primary_key=True, serialize=False)),
                ('nombre_rol', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Titulo',
            fields=[
                ('id_titulo', models.BigAutoField(primary_key=True, serialize=False)),
                ('nombre_titulo', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id_solicitud', models.BigAutoField(primary_key=True, serialize=False)),
                ('recibidor', models.IntegerField(null=True)),
                ('fk_id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sala',
            fields=[
                ('id_sala', models.BigAutoField(primary_key=True, serialize=False)),
                ('nombre_sala', models.CharField(max_length=200)),
                ('fk_id_grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Gaminghub.grupo')),
            ],
        ),
        migrations.CreateModel(
            name='RegistroGrupo',
            fields=[
                ('id_registro', models.BigAutoField(primary_key=True, serialize=False)),
                ('fk_id_grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Gaminghub.grupo')),
                ('fk_id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Puntaje',
            fields=[
                ('id_puntaje', models.BigAutoField(primary_key=True, serialize=False)),
                ('puntos', models.IntegerField(null=True)),
                ('fk_id_titulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Gaminghub.titulo')),
                ('fk_id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Publicacion',
            fields=[
                ('id_publicacion', models.BigAutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=60)),
                ('contenido', models.CharField(max_length=200)),
                ('multimedia', models.FileField(upload_to='multimedia/')),
                ('fecha_creacion', models.DateField()),
                ('dislike', models.ManyToManyField(blank=True, related_name='dislike', to=settings.AUTH_USER_MODEL)),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('like', models.ManyToManyField(blank=True, related_name='like', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PerfilUsuario',
            fields=[
                ('id_perfil', models.BigAutoField(primary_key=True, serialize=False)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('edad', models.IntegerField(null=True)),
                ('genero', models.CharField(max_length=20, null=True)),
                ('descripcion', models.CharField(max_length=200, null=True)),
                ('avatar', models.ImageField(upload_to='')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id_notificacion', models.BigAutoField(primary_key=True, serialize=False)),
                ('info', models.TextField(max_length=300, null=True)),
                ('fecha_creacion', models.DateField(auto_now_add=True, null=True)),
                ('tipo', models.IntegerField(null=True)),
                ('fk_id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notificaciones_enviador', to=settings.AUTH_USER_MODEL)),
                ('fk_recibidor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notificaciones_recibidor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Miembro',
            fields=[
                ('id_miembro', models.BigAutoField(primary_key=True, serialize=False)),
                ('fk_id_grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Gaminghub.grupo')),
                ('fk_id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MensajeGrupo',
            fields=[
                ('id_mensajeGrupo', models.BigAutoField(primary_key=True, serialize=False)),
                ('contenido', models.CharField(max_length=400, null=True)),
                ('multimedia', models.FileField(null=True, upload_to='multimedia/')),
                ('fecha_envio', models.DateTimeField(auto_now_add=True)),
                ('fk_id_sala', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Gaminghub.sala')),
                ('remitente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id_mensaje', models.BigAutoField(primary_key=True, serialize=False)),
                ('contenido', models.TextField(null=True)),
                ('multimedia', models.FileField(null=True, upload_to='multimedia/')),
                ('estado', models.IntegerField(null=True)),
                ('fecha_envio', models.DateTimeField(auto_now_add=True)),
                ('destinatario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mensajes_recibidos', to=settings.AUTH_USER_MODEL)),
                ('remitente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mensajes_enviados', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id_comentario', models.BigAutoField(primary_key=True, serialize=False)),
                ('descripcion', models.TextField(max_length=200)),
                ('fecha_creacion', models.DateField(auto_now_add=True, null=True)),
                ('fk_id_publicacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Gaminghub.publicacion')),
                ('fk_id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
