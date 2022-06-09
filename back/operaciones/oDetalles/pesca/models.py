from django.db import models
from operaciones.models import DetalleOperacion

#COSAS QUE PASAN DURANTE LA OPERATORIA
class DetalleRedArrastre(DetalleOperacion): #tienen el atributo "operacion" porque DetalleOperacion lo posee
    nro_lance = models.PositiveIntegerField(null=True)
    rumbo = models.CharField(max_length=5, null=True)
    vel_arras = models.FloatField(null=True)
    dist_arras = models.FloatField(null=True) #para obtenner el area barrida
    aber_vert = models.FloatField(null=True)
    cab_filad = models.FloatField(null=True)
    dist_alas = models.FloatField(null=True) # = (dist_e_port x cuerpo_red (RedArrastre)) / (cuerpo_ red (RedArrastre) +bridas (RedArrastre) + patentes (RedArrastre)) 
    ang_pala_helice = models.FloatField(null=True)
    dist_e_por = models.FloatField(null=True)
    tension_red = models.FloatField(null=True)
    area_barrida = models.FloatField(null=True) # = dist_arras x (dist_alas/1852)
    observacion = models.CharField(max_length=150, null=True)


class DetallePalangre(DetalleOperacion):
    linea_madre_mat = models.FloatField(null=True)
    linea_madre_largo = models.FloatField(null=True)
    linea_madre_tramo = models.FloatField(null=True)
    brazolada_largo = models.FloatField(null=True)
    brazolada_separacion = models.FloatField(null=True)
    brazolada_nro_tramo = models.FloatField(null=True)
    anzuelos_nro_total = models.FloatField(null=True)
    anzuelos_con_carnada = models.FloatField(null=True)
    anzuelos_sin_carnada = models.FloatField(null=True)
    carnada = models.CharField(max_length=100, null=True)
    observacion = models.CharField(max_length=150, null=True)

