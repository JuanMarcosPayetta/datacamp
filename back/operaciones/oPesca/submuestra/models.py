from django.db import models
from django.core.validators import MinValueValidator
from operaciones.oPesca.captura.models import Captura



class Submuestra(models.Model):
    captura = models.ForeignKey(Captura, on_delete=models.CASCADE)
    nro_ejemplar = models.IntegerField(null=True,
                                       blank=True,
                                       validators=[MinValueValidator(0)])
    largo_total = models.DecimalField(max_digits=12,
                                      decimal_places=4,
                                      null=True,
                                      blank=True)
    # En caso de ser True significa que esta en cms.
    unidad_lt = models.BooleanField(default=False)
    sexo = models.IntegerField(null=True,
                               blank=True)
    peso_total = models.DecimalField(max_digits=12,
                                     decimal_places=4,
                                     null=True,
                                     blank=True)
    # En caso de ser True significa que es en gramos.
    unidad_p = models.BooleanField(default=False)

    class Meta:
        abstract = True

    @classmethod
    def getInstanciasSubmuestras(cls, captura):
        classes = cls.__subclasses__()
        for c in classes:
            try:
                if c.objects.filter(captura=captura).exists():
                    return c.objects.filter(captura=captura)
            except:
                return False

class ContenidoEstomacal(models.Model):
    contenido_estomacal = models.DecimalField(max_digits=12,
                                              decimal_places=2,
                                              null=True,
                                              blank=True)
    pieza = models.DecimalField(max_digits=12,
                                decimal_places=4,
                                null=True,
                                blank=True)
    largo = models.DecimalField(max_digits=12,
                                decimal_places=4,
                                null=True,
                                blank=True)
    peso = models.DecimalField(max_digits=12,
                               decimal_places=4,
                               null=True,
                               blank=True)

class SubmuestraOsteictios(Submuestra):
    largo_standard = models.DecimalField(max_digits=12,
                                         decimal_places=2,
                                         null=True,
                                         blank=True)
    estadio_gonadal = models.IntegerField(null=True, blank=True)
    peso_gonadal = models.IntegerField(null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    replecion_estomacal = models.IntegerField(null=True, blank=True)
    # Si es True significa que guardo material
    material_guardado = models.BooleanField(default=False)
    contenido_estomacal = models.ManyToManyField(ContenidoEstomacal)


ESTADO_CAPARAZON = (
    ('1', 'Mudando'),
    ('2', 'Flexible'),
    ('3', 'Nuevo'),
    ('4', 'Medio'),
    ('5', 'Viejo'),
    ('6', 'Muy viejo'),
)

ESTADO_HUEVOS = (
    ('1', 'Con huevos'),
    ('2', 'Sin huevos'),
    ('3', 'Desovando'),
    ('4', 'Desovada')
)
class SubmuestraCrustaceos(Submuestra):
    caparazon_largo = models.DecimalField(max_digits=12,
                                          decimal_places=2,
                                          null=True,
                                          blank=True)
    caparazon_ancho = models.DecimalField(max_digits=12,
                                          decimal_places=2,
                                          null=True,
                                          blank=True)
    caparazon_estado = models.IntegerField(choices=ESTADO_CAPARAZON,
                                           null=True,
                                           blank=True)
    mero_largo = models.DecimalField(max_digits=12,
                                     decimal_places=2,
                                     null=True,
                                     blank=True)
    quela_largo = models.DecimalField(max_digits=12,
                                      decimal_places=2,
                                      null=True,
                                      blank=True)
    quela_ancho = models.DecimalField(max_digits=12,
                                      decimal_places=2,
                                      null=True,
                                      blank=True)
    huevos = models.IntegerField(choices=ESTADO_HUEVOS,
                                 null=True, blank=True)
    porcentaje_huevos = models.IntegerField(null=True, blank=True)
    abdomen_largo = models.DecimalField(max_digits=12,
                                        decimal_places=2,
                                        null=True,
                                        blank=True)
    abdomen_ancho = models.DecimalField(max_digits=12,
                                        decimal_places=2,
                                        null=True,
                                        blank=True)
    porcentaje_carne = models.IntegerField(null=True, blank=True)
    envergadura = models.DecimalField(max_digits=12,
                                      decimal_places=2,
                                      null=True,
                                      blank=True)
    observacion = models.CharField(max_length=250,
                                   null=True,
                                   blank=True)

class SubmuestraCefalopodos(Submuestra):
    estadio_gonadal = models.IntegerField(null=True,
                                          blank=True,
                                          validators=[MinValueValidator(0)])
    replecion_estomacal = models.IntegerField(null=True,
                                              blank=True,
                                              validators=[MinValueValidator(0)])
    peso_estom = models.DecimalField(null=True,
                                     blank=True,
                                     max_digits=12,
                                     decimal_places=4,
                                     validators=[MinValueValidator(0)])
    peso_mues = models.DecimalField(null=True,
                                    blank=True,
                                    max_digits=12,
                                    decimal_places=4,
                                    validators=[MinValueValidator(0)])

class SubMuestraCondrictios(Submuestra):
    estadio = models.IntegerField(null=True,
                                  blank=True)
    a_disco = models.IntegerField(null=True,
                                  blank=True)
    peso_tot = models.IntegerField(null=True,
                                   blank=True)
    l_ce_au = models.IntegerField(null=True,
                                  blank=True)
    l_ci_ag = models.IntegerField(null=True,
                                  blank=True)
    d_max_fo = models.IntegerField(null=True,
                                   blank=True)
    lpro_em_iz = models.IntegerField(null=True,
                                     blank=True)
    n_em_ma_iz = models.IntegerField(null=True,
                                     blank=True)
    n_em_he_iz = models.IntegerField(null=True,
                                     blank=True)
    n_em_in_iz = models.IntegerField(null=True,
                                     blank=True)
    lpro_em_de = models.IntegerField(null=True,
                                     blank=True)
    n_em_ma_de = models.IntegerField(null=True,
                                     blank=True)
    n_em_he_de = models.IntegerField(null=True,
                                     blank=True)
    n_em_in_de = models.IntegerField(null=True,
                                     blank=True)
    g_reple = models.IntegerField(null=True,
                                  blank=True)
    mat_guarda = models.CharField(max_length=40,
                                  null=True,
                                  blank=True)
    observaciones = models.BooleanField(default=False)
    contenido_estomacal = models.ManyToManyField(ContenidoEstomacal)

class EmbrionesCondrictios(models.Model):
    submuestra = models.ForeignKey(SubMuestraCondrictios,
                                   on_delete=models.CASCADE,
                                   null=False)
    observaciones = models.CharField(max_length=100)
    total_izq = models.IntegerField(null=True, blank=True)
    total_der = models.IntegerField(null=True, blank=True)
    num_ej = models.IntegerField(null=True, blank=True)

class DetalleEmbrionesCondrictios(models.Model):
    embrion = models.ForeignKey(EmbrionesCondrictios,
                                on_delete=models.CASCADE,
                                null=False)
    lt_emb_i = models.IntegerField(null=True, blank=True)
    sexo_i = models.IntegerField(null=True, blank=True)
    lt_emb_d = models.IntegerField(null=True, blank=True)
    sexo_d = models.IntegerField(null=True, blank=True)