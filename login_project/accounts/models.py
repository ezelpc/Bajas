from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    rol = models.CharField(
        max_length=100,
        choices=[
            ('admin', 'Admin'),
            ('usuario', 'Usuario'),
        ],
        default='usuario'
    )  # Rol del usuario
    email = models.EmailField(unique=True)  # Correo electrónico único

    # Redefinir los campos para evitar conflictos
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",  # Nombre único para evitar conflictos
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",  # Nombre único para evitar conflictos
        blank=True
    )

    def __str__(self):
        return self.username

class QRCode(models.Model):
    folio = models.CharField(max_length=100, unique=True)  # Folio único
    usado = models.BooleanField(default=False)  # Estado del QR (usado o no)

    def __str__(self):
        return self.folio

class Formulario(models.Model):
    pzas = models.PositiveIntegerField(default=0)  # Número de piezas registradas
    descripcion = models.TextField(blank=True, null=True)  # Descripción del equipo
    modelo = models.CharField(max_length=255, blank=True, null=True)  # Modelo del equipo
    numero_serie = models.CharField(max_length=255, blank=True, null=True)  # Número de serie
    activo_smn = models.CharField(max_length=255, blank=True, null=True)  # Activo SMN
    sucursal = models.CharField(max_length=255, blank=True, null=True)  # Sucursal
    qr = models.ForeignKey(QRCode, on_delete=models.CASCADE)  # Relación con el QR

    def __str__(self):
        return f"{self.qr.folio} - {self.descripcion}"
