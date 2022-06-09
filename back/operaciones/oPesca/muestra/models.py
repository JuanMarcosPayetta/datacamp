from django.db import models
from django.core.validators import MinValueValidator
from operaciones.oPesca.captura.models import Captura


class Muestra(models.Model):
    # Recordar que todos los valores numericos corresponden a Centimetros!
    captura = models.ForeignKey(Captura, on_delete=models.CASCADE)
    talla_inferior = models.IntegerField(null=True,
                                         blank=True,
                                         validators=[MinValueValidator(1)])
    talla_superior = models.IntegerField(null=True,
                                         blank=True,
                                         validators=[MinValueValidator(1)])
    peso = models.DecimalField(max_digits=12,
                               decimal_places=4,
                               null=True)
    ej_kg = models.DecimalField(max_digits=12,
                                decimal_places=4,
                                null=True)

    def getDetallesXMuestra(self):
        return DetalleMuestra.objects\
                   .filter(muestra=self)\
                   .order_by('talla')

    def get_cant_kg(self):
        detalles = DetalleMuestra.objects.filter(muestra=self)
        if detalles:
            cant_ejem = 0
            for detalle in detalles:
                if detalle.cant_macho:
                    cant_ejem += detalle.cant_macho
                if detalle.cant_hembra:
                    cant_ejem += detalle.cant_hembra
                if detalle.cant_indet:
                    cant_ejem += detalle.cant_indet
            total = cant_ejem / self.captura.kg
            return total
        else: return None

class DetalleMuestra(models.Model):
    muestra = models.ForeignKey(Muestra,
                                on_delete=models.CASCADE)
    cant_macho = models.IntegerField(null=True,
                                     blank=True,
                                     validators=[MinValueValidator(0)])
    cant_hembra = models.IntegerField(null=True,
                                      blank=True,
                                      validators=[MinValueValidator(0)])
    cant_indet = models.IntegerField(null=True,
                                     blank=True,
                                     validators=[MinValueValidator(0)])
    # Este field es para las muestras que no son ni machos hembras o ind
    # Los indet es xq son menores que maduros y no se sabe el sexo
    # Estos totales es xq no se sabe el sexo ya que puede venir
    # dañado el ejemplar
    cant_totales = models.IntegerField(null=True,
                                       blank=True,
                                       validators=[MinValueValidator(0)])
    talla = models.IntegerField(null=True,
                                blank=True,
                                validators=[MinValueValidator(0)])
    estad_gonadales = models.IntegerField(null=True,
                                          blank=True)
    ancho_disco = models.IntegerField(null=True,
                                      blank=True,
                                      validators=[MinValueValidator(0)])


class MuestraLangostino(models.Model):
    captura = models.ForeignKey(Captura, on_delete=models.CASCADE)
    talla_inferior = models.IntegerField(null=True,
                                         blank=True,
                                         validators=[MinValueValidator(1)])
    talla_superior = models.IntegerField(null=True,
                                         blank=True,
                                         validators=[MinValueValidator(1)])
    peso = models.DecimalField(max_digits=12,
                               decimal_places=4,
                               null=True)
    ej_kg = models.DecimalField(max_digits=12,
                                decimal_places=4,
                                null=True)
    # Recordar que todos los valores numericos corresponden a Milimetros!
    inicio_talla_madura = models.IntegerField(null=True,
                                              blank=True,
                                              validators=[MinValueValidator(0)])
    peso_machos = models.DecimalField(max_digits=12,
                                      decimal_places=4,
                                      null=True)
    peso_hembras_inmaduras = models.DecimalField(max_digits=12,
                                                 decimal_places=4,
                                                 null=True)
    peso_hembras_maduras = models.DecimalField(max_digits=12,
                                               decimal_places=4,
                                               null=True)
    peso_hembras_impregnadas = models.DecimalField(max_digits=12,
                                                   decimal_places=4,
                                                   null=True)

class DetalleMuestraLangostino(models.Model):
    muestra = models.ForeignKey(MuestraLangostino,
                                on_delete=models.CASCADE)
    talla = models.IntegerField(null=True,
                                blank=True,
                                validators=[MinValueValidator(0)])
    cant_macho_inmaduro = models.IntegerField(null=True,
                                              blank=True,
                                              validators=[MinValueValidator(0)])
    cant_macho_maduro = models.IntegerField(null=True,
                                            blank=True,
                                            validators=[MinValueValidator(0)])
    cant_hembra_inmadura = models.IntegerField(null=True,
                                               blank=True,
                                               validators=[MinValueValidator(0)])
    cant_hembra_madura = models.IntegerField(null=True,
                                             blank=True,
                                             validators=[MinValueValidator(0)])
    cant_impregnadas = models.IntegerField(null=True,
                                           blank=True,
                                           validators=[MinValueValidator(0)])
    cant_indet = models.IntegerField(null=True,
                                     blank=True,
                                     validators=[MinValueValidator(0)])
