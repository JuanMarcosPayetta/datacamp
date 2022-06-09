from django.db import models
from estaciones.models import Operacion


class ResultadoOperacional(models.Model):
    operacion = models.ForeignKey(Operacion,
                                  on_delete=models.CASCADE)

    class Meta:
        abstract = True

class DetalleOperacion(models.Model):
    operacion = models.ForeignKey(Operacion,
                                  on_delete=models.CASCADE)

    def __unicode__(self):
        return "Operacion: " \
               + str(self.operacion) \

    class Meta:
        abstract = True