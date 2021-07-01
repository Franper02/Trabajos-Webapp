from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from django.db.models.signals import post_save


class Usuario(AbstractUser):
    pass


class Tps(models.Model):

    users = models.ManyToManyField(
        Usuario,  through='Tpsterminados')
    titulo = models.CharField(max_length=100)

    TECNOLOGIA_DE_LA_FABRICACION = 'TDF'
    MANTENIMIENTO_Y_REPARACION_DE_EQUIPOS = 'MYRDE'
    MAQUINAS_ELECTRICAS_Y_ENSAYOS = 'MEYE'
    SEGURIDAD_E_HIGIENE_INDUSTRIAL = 'SEHI'
    LABORATORIO_DE_ENSAYOS_INDUSTRIALES = 'LDEI'
    INSTALACIONES_INDUSTRIALES = 'II'
    RELACIONES_HUMANAS = 'RH'
    TALLER_DE_ELECTROMECANICA = 'TE'
    ORGANIZACION_INDUSTRIAL = 'OI'
    INSTALACIONES_ELECTRICAS = 'IE'
    EDUCACION_FISICA = 'EF'
    EQUIPOS_Y_APARATOS_DE_MANIOBRA_Y_TRANSPORTE = 'EYADMYT'

    MATERIAS_CHOICES = [
        (TECNOLOGIA_DE_LA_FABRICACION, 'Tecnologia de la fabricación'),
        (MANTENIMIENTO_Y_REPARACION_DE_EQUIPOS, 'Mantenimiento y R de equipos'),
        (MAQUINAS_ELECTRICAS_Y_ENSAYOS, 'Máquinas eléctricas y ensayos'),
        (SEGURIDAD_E_HIGIENE_INDUSTRIAL, 'Seguridad e higiene industrial'),
        (LABORATORIO_DE_ENSAYOS_INDUSTRIALES,
         'Laboratorio de ensayos industriales'),
        (INSTALACIONES_INDUSTRIALES, 'Instalaciones industriales'),
        (RELACIONES_HUMANAS, 'Relaciones humanas'),
        (TALLER_DE_ELECTROMECANICA, 'Taller de electromecánica'),
        (ORGANIZACION_INDUSTRIAL, 'Organización industrial'),
        (INSTALACIONES_ELECTRICAS, 'Instalaciones eléctricas'),
        (EDUCACION_FISICA, 'Educacion fisica'),
        (EQUIPOS_Y_APARATOS_DE_MANIOBRA_Y_TRANSPORTE,
         'Equipos y aparatos de maniobra y transporte')
    ]
    materia = models.CharField(
        max_length=8, choices=MATERIAS_CHOICES, default=None)

    fecha_actual = models.DateField(default=timezone.now)
    fecha_entrega = models.DateField(auto_now=False, auto_now_add=False)

    material = models.URLField()
    consignas = models.URLField()

    def __str__(self):
        return self.titulo


def taskdone(sender, instance, **kwargs):
    for user in Usuario.objects.all():
        Tpsterminados.objects.create(user=user, tps=Tps.objects.last())


post_save.connect(taskdone, sender=Tps)


class Tpsterminados(models.Model):
    user = models.ForeignKey(Usuario, on_delete=CASCADE)
    tps = models.ForeignKey(Tps, on_delete=CASCADE)
    status = models.BooleanField(default=True)
