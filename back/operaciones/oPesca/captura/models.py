from django.db import models
from estaciones.models import EstacionGeneral
from operaciones.especies.models import Especie
from operaciones.models import Operacion,\
                               ResultadoOperacional
from operaciones.oDetalles.pesca.models import DetalleRedArrastre,\
                                               DetallePalangre

class ResultadoPesca(ResultadoOperacional): 
    nro_lance = models.PositiveIntegerField(null=True)

    class Meta:
        abstract = True

class Captura(ResultadoPesca): #TIENE "OPERACION" XQ LO HEREDA!!
    # El codigo corresponde al usado en la bd de especies. Cod de INIDEP
    especie = models.ForeignKey(Especie,
                                on_delete=models.CASCADE)
    especie_desc = models.CharField(max_length=255)
    kg = models.DecimalField(max_digits=12,
                             decimal_places=4)
    cantidadXkilo = models.DecimalField(max_digits=12,
                                        decimal_places=4,
                                        null=True)
    cant_ejemplares = models.IntegerField(null=True,
                                          blank=True)


    @staticmethod
    def getCapturaTotalxEstacion(estacionGeneral):
        listCapturas = Captura.objects.filter(
                          operacion__estacion_general=estacionGeneral)
        cap_total = 0
        for captura in listCapturas:
            cap_total = cap_total + captura.kg
        return cap_total

    @staticmethod
    def getCapturasxCampania(oCampania): #todas las capturas, de cada operacion, de cada estacion de una campañia determinada
        capturas = []
        for estacion_general in EstacionGeneral.get_estaciones_por_campania(oCampania):
            for operacion in Operacion.get_operaciones(estacion_general.pk):
                for captura in Captura.objects\
                                      .filter(operacion=operacion)\
                                      .order_by('nro_lance'):# hace operacion buscada, igual a la operacion de la captura (porque herede ese atributo)
                    capturas.append(captura)
        return capturas

        #ESTE ES EL MISMO CODIGO QUE FUNCIONA (juan):  capturas_objs=Captura.objects.filter(operacion__estacion_general__etapa__campania_id=campania.id)


    @staticmethod
    def getEspeciesCapturasxCampania(oCampania):
        capturas = Captura.getCapturasxCampania(oCampania)
        list_especies = []
        [
            list_especies.append(captura.especie)
            for captura in capturas
            if captura.especie not in list_especies
        ]
        list_especies.sort(key=lambda esp: esp.nombre_cientifico)
        return list_especies

    @staticmethod
    def getCantLancesConCapturaXEstrato(estrato):
        return Captura.objects\
                            .filter(operacion_id__estacion_general_id__estrato_id=estrato)\
                            .values('nro_lance').distinct().count()

    def getDetalleOperacion(self):
        red_arrastre = DetalleRedArrastre.objects\
                                           .filter(operacion=self.operacion)
        if red_arrastre:
            return red_arrastre[0]
        else:
            red_palangre = DetallePalangre.objects\
                                            .filter(operacion=self.operacion)
            if red_palangre:
                return red_palangre[0]
            else: return None

    @staticmethod
    def getCapturaxEstacion(oEg):
        capts = Captura.objects\
                       .filter(operacion__estacion_general=oEg)
        return capts

    @staticmethod
    def getCapturaxEstrato(oEstrato):
        capts = Captura.objects\
                       .filter(operacion__estacion_general__estrato=oEstrato)\
                       .order_by('nro_lance')
        return capts