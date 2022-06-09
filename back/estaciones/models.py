from django.db import models

from campanias.models import Etapa, Estrato, MuestreadorABordo, Parametro


class EspacioTemporal(models.Model):
    fecha_hora = models.DateTimeField(null=True, blank=True)
    lat=models.FloatField(null=True, blank=False)
    lon=models.FloatField(null=True, blank=False)

    def __str__(self):
        return str(self.lat)+':'+str(self.lon)

class EstacionGeneral(models.Model):
    numero_plan = models.IntegerField(null=True)
    etapa = models.ForeignKey(Etapa,
                              related_name='estaciones',
                              on_delete=models.CASCADE)
    espacio_tiempo = models.ForeignKey(EspacioTemporal,
                                       blank=True,
                                       null=True,
                                       on_delete=models.CASCADE)
    estrato = models.ForeignKey(Estrato,
                                blank=True,
                                null=True,
                                on_delete=models.SET_NULL,
                                related_name='estratos')
    nro_transecta = models.CharField(max_length=10,
                                     blank=True,
                                     null=True)
    nro_estacion_barco = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.nro_estacion_barco)

    @staticmethod
    def get_estaciones_por_campania(campania):
        return EstacionGeneral.objects\
            .filter(etapa__campania=campania)\
            .order_by('nro_estacion_barco')

    @classmethod
    def get_estaciones_por_list_de_pk(lista_pk_eg):
        return EstacionGeneral.objects.filter(pk__in=lista_pk_eg)

    def get_operaciones(self):
        return Operacion.objects.filter(estacion_general=self) #estacion_general_id = id que le paso por parametro

    @staticmethod
    def get_estaciones_por_fecha(campania, fecha_init, fecha_fin):
        list_estaciones = []
        for estacion in EstacionGeneral.get_estacionesXcampania(campania):
            if estacion.espacio_tiempo.fecha_hora:
                fecha = estacion.espacio_tiempo.fecha_hora.date()
                if fecha >= fecha_init and fecha <= fecha_fin:
                    list_estaciones.append(estacion)
        return list_estaciones

    @staticmethod
    def get_estaciones_por_muestreador(campania, muestrador_bordo):
        list_estaciones = []
        for estacion in EstacionGeneral.get_estaciones_por_campania(campania):
            for operacion in EstacionGeneral.get_operaciones(estacion.pk):
                if operacion.muestreador == muestrador_bordo:
                    list_estaciones.append(estacion)
        return list_estaciones

    def delete_estacionYdatos(self):
        for operacion in Operacion.objects.filter(estacion_general_id=self.pk):
            if operacion.inicio_espacio_temporal:
                operacion.inicio_espacio_temporal.delete()
            if operacion.fin_espacio_temporal:
                operacion.fin_espacio_temporal.delete()
            operacion.delete()
            if self.dato_ambiental():
                self.dato_ambiental.delete()

class DatoAmbiental(models.Model):
    presion = models.FloatField(blank=True, null=True)
    viento_dir = models.IntegerField(blank=True, null=True)
    viento = models.IntegerField(blank=True, null=True)
    temperatura_bs = models.FloatField(blank=True, null=True)
    temperatura_bh = models.FloatField(blank=True, null=True)
    nubes_cant = models.IntegerField(blank=True, null=True)
    nubes_tipo = models.IntegerField(blank=True, null=True)
    visibilidad = models.IntegerField(blank=True, null=True)
    mar_estado = models.IntegerField(blank=True, null=True)
    mar_direccion = models.IntegerField(blank=True, null=True)
    profundidad = models.FloatField(blank=True, null=True)
    estacion_general = models.ForeignKey(EstacionGeneral,
                                         related_name='dato_ambiental',
                                         on_delete=models.CASCADE)

    def __str__(self):
        return str(self.estacion_general)

class Operacion(models.Model):
    muestreador = models.ForeignKey(MuestreadorABordo,
                                    on_delete=models.CASCADE)
    estacion_general = models.ForeignKey(EstacionGeneral,
                                         related_name='operaciones',
                                         on_delete=models.CASCADE)
    inicio_espacio_temporal = models.ForeignKey(EspacioTemporal,
                                                related_name='espacio_inicial',
                                                blank=True,
                                                null=True,
                                                on_delete=models.SET_NULL)
    fin_espacio_temporal = models.ForeignKey(EspacioTemporal,
                                             related_name='espacio_final',
                                             blank=True,
                                             null=True,
                                             on_delete=models.SET_NULL)
    exitosa = models.BooleanField(default=True)
    observaciones = models.TextField(max_length=1500,
                                     blank=True,
                                     null=True)
    confirmado = models.BooleanField(default=False)

    def __str__(self):
        return str(self.estacion_general)+':'+self.muestreador.muestreador.nombre

    @staticmethod
    def get_list_estaciones_X_muestreador(oCampania, oMuestreador):
        lista=[]
        operaciones=Operacion.objects.filter(estacion_general__etapa__campania=oCampania,
                                             muestreador=oMuestreador)
        for o in operaciones:
            lista.append(o.estacion_general.id)
        return lista

    @staticmethod
    def get_operacionesXmuestreador(oCampania, oMuestreador):
        return Operacion.objects.filter(estacion_general__etapa__campania=oCampania,
                                        muestreador = oMuestreador)

    @staticmethod
    def get_OperacionesXcamp(ocampania):
        lista=[]
        operaciones=Operacion.objects.filter(estacion_general__etapa__campania=ocampania)
        for op in operaciones:
            lista.append(op.id)
        return lista

    def return_campania(self):
        return self.estacion_general.etapa.campania

    @staticmethod
    def get_operaciones(pk_estacion):
        return Operacion.objects.filter(estacion_general_id=pk_estacion)

class ParametroPorOp(models.Model):
    operacion = models.ForeignKey(Operacion,
                                  related_name='parametros',
                                  on_delete=models.CASCADE)
    parametro = models.ManyToManyField(Parametro,
                                       related_name='para')

    def __str__(self):
        return str(self.parametro.get())
