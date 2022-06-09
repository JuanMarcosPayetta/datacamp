from django.db import models

class Institucion(models.Model):
    descripcion = models.TextField(max_length=75, null=True, blank=True)
    codigo = models.CharField(max_length=10)
    comentarios = models.TextField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.codigo + ' '+ self.descripcion

class RolPersona(models.Model):
    codigo = models.CharField(max_length=5)
    descripcion = models.TextField(max_length=40)

    def __str__(self):
        return self.descripcion

class Laboratorio(models.Model):
    descripcion = models.CharField(max_length=140, null=True)
    nombre = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.descripcion

class Persona(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    mail = models.CharField(max_length=40)
    dni = models.CharField(max_length=10)
    externo = models.BooleanField(default=False)
    instituciones = models.ManyToManyField(Institucion)
    laboratorios = models.ManyToManyField(Laboratorio)

    def __str__(self):
        return self.nombre + ' ' + self.apellido