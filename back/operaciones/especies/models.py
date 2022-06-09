# -*- coding: UTF-8 -*-

from django.db import models

# Create your models here.
class Orden(models.Model):
    cod_inidep = models.CharField(max_length=10)
    nombre = models.CharField(max_length=15)

class Especie(models.Model):
    cod_inidep = models.CharField(max_length=10)
    cod_fao_alfa3 = models.CharField(max_length=3, null=True, blank=True)
    cod_fao_taxonomico = models.CharField(max_length=13, null=True, blank=True)
    nombre_cientifico = models.CharField(max_length=255)
    nombre_anterior_1 = models.CharField(max_length=255, null=True, blank=True)
    nombre_anterior_2 = models.CharField(max_length=255, null=True, blank=True)
    orden = models.ForeignKey(Orden, null=True, blank=True, on_delete=models.SET_NULL)

    @property
    def nombre_vulgar_1(self):
        try:
            nv=Nombre_Vulgar_Especie.objects.filter(especie=self)
            if nv[0]:
                return nv[0]
        except:
            return ''

    def __unicode__(self):
        return str(self.nombre_cientifico)

    def __str__(self):
        return str(self.nombre_cientifico)

class Nombre_Vulgar_Especie(models.Model):
    nombre = models.CharField(max_length=255)
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.nombre

    def __str__(self):
        return str(self.nombre)

