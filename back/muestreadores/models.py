# En este models se define: Detalles de Muestreadores.
from django.db import models
from campanias.models import MuestreadorABordo

class DetalleMuestreadores(models.Model):
    descripcion = models.CharField(max_length=250, null=True, blank=True)
    muestreador = models.ForeignKey(MuestreadorABordo,on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def get_type_detalle(self):
        if self.muestreador.muestreador.codigo == 'REDARRAFON':
            return self.__class__