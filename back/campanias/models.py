from django.contrib.auth.models import User
from django.db import models

#Local Imports
from personas.models import Laboratorio, Persona, RolPersona


class Programa(models.Model):
    codigo = models.CharField(max_length=15, null=True)
    descripcion = models.TextField(max_length=140, null=True)

class TipoObjetivo(models.Model):
    codigo = models.CharField(max_length=6, null=True)
    descripcion = models.TextField(max_length=140)

    def __str__(self):
        return self.descripcion

    def returnEtiquetasXCodigo(self):
        return EtiquetaObjetivo.objects.filter(tipo__id=self.pk)

class EtiquetaObjetivo(models.Model):
    codigo = models.CharField(max_length=6)
    descripcion = models.TextField(max_length=140)
    tipo = models.ForeignKey(TipoObjetivo,
                             on_delete=models.CASCADE,
                             null=True)

    def __str__(self):
        return self.descripcion

class Parametro(models.Model):
    codigo = models.CharField(max_length=6)
    codigo_ICES = models.CharField(max_length=6, null=True)
    codigo_ISO = models.CharField(max_length=6, null = True)
    descripcion = models.TextField(max_length=140)
    padre = models.ForeignKey('self',
                              blank=True,
                              null=True,
                              on_delete=models.SET_NULL)

    def __str__(self):
        return self.descripcion

class Puerto(models.Model):
    nombre=models.CharField(max_length=50)
    lat=models.FloatField(null=True)
    lon=models.FloatField(null=True)

    def __str__(self):
        return self.nombre

    def __repr__(self):
        return self.nombre

class TipoPlataforma(models.Model):
    descripcion = models.CharField(max_length=140)
    codigo_ICES = models.CharField(max_length=6, null=True)

    def __str__(self):
        return self.descripcion

class Pais(models.Model):
    nombre = models.CharField(max_length=50)
    iso = models.CharField(max_length=4)

    def __str__(self):
        return self.iso + ' ' + self.nombre

class Plataforma(models.Model):
    codigo_ICES = models.CharField(max_length=4)
    codigo_bardo = models.CharField(max_length=35, null=True)
    nombre=models.CharField(max_length=30)
    matricula=models.CharField(max_length=7, null=True)
    sradial=models.CharField(max_length=7,
                             null=True,
                             blank=True)
    mat_sat=models.CharField(max_length=7,
                             null=True,
                             blank=True)
    pais = models.ForeignKey(Pais,
                             null=True,
                             blank=True,
                             on_delete=models.SET_NULL)
    tipo = models.ForeignKey(TipoPlataforma,
                             null=True,
                             blank=True,
                             on_delete=models.SET_NULL)
    descripcion = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.nombre

class TipoMuestreador(models.Model):
    codigo = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=140) #Titulo (ejemplo: Redes de Pesca)

    def __str__(self):
        return self.descripcion

class Muestreador(models.Model):
    nombre = models.CharField(max_length=300) #Nombre que aparece al dar click en un Tipo (descripcion del TipoMuestreador)
    observaciones = models.CharField(max_length=150,
                                     blank=True,
                                     null=True)
    codigo = models.CharField(max_length=10)
    muestra = models.BooleanField(default=False)
    continuo = models.BooleanField(default=False)
    parametros = models.ManyToManyField(Parametro)
    tipo_muestreador = models.ForeignKey(TipoMuestreador,
                                         null=False,
                                         on_delete=models.CASCADE, related_name="muestreador")
    generico = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class Campania(models.Model):
    codigo = models.CharField(max_length=20)
    codigo_interno = models.CharField(max_length=20)
    descripcion = models.TextField(max_length=500,
                                   null=True,
                                   blank=True)
    titulo = models.CharField(max_length=350)
    objetivos_principales = models.TextField(max_length=5000,
                                             blank=True,
                                             null=True)
    objetivos_secundarios = models.TextField(max_length=5000,
                                             blank=True,
                                             null=True)
    programa = models.ForeignKey(Programa,
                                 null=True,
                                 on_delete=models.SET_NULL)
    objetivos_etiqueta = models.ManyToManyField(EtiquetaObjetivo)
    plataforma = models.ManyToManyField(Plataforma, related_name='plataforma')

    def __str__(self):
        return self.codigo + ' ' + self.titulo

    def fecha_salida(self):
        primer_etapa = self.primer_etapa()
        if primer_etapa:
            return primer_etapa.fecha_init

    def fecha_llegada(self):
        ultima_etapa = self.ultima_etapa()
        if ultima_etapa:
            return ultima_etapa.fecha_fin

    def primer_etapa(self):
        if Etapa.objects.filter(campania=self.pk).exists():
            return Etapa.objects.filter(campania=self.pk).order_by('fecha_init')[0]

    def ultima_etapa(self):
        if Etapa.objects.filter(campania=self.pk).exists():
            return Etapa.objects.filter(
                campania=self.pk)\
                .order_by('fecha_init').last()

    def get_estaciones(self):
        estaciones=[]
        for etapa in self.etapas.all():
            for estacion in etapa.estaciones.all():
                estaciones.append(estacion)
        return estaciones

    def return_etapa(self, fecha):
        # This def always needs an instance of date.
        for etapa in self.etapas.all():
            if (fecha >= etapa.fecha_init and
                    fecha <= etapa.fecha_fin):
                return etapa

    def fecha_ok(self, fecha):
        # Esta def debe recibir siempre una variable fecha de tipó date para funcionar
        for etapa in Etapa.objects.filter(campania=self):
            if (etapa.fecha_init < fecha and
                        fecha < etapa.fecha_fin):
                return True
        return False
    
class Estrato(models.Model):
    numero = models.IntegerField()
    area = models.FloatField()
    cuadricula = models.IntegerField()
    zona = models.TextField(max_length=340, null=True)
    campania = models.ForeignKey(Campania,
                                 related_name='estratos',
                                 null=False,
                                 on_delete=models.CASCADE)

    def __str__(self):
        return str(self.numero)

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    campania = models.ForeignKey(Campania,
                                 null=False,
                                 on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class MuestreadorABordo(models.Model):
    campania = models.ForeignKey(Campania,
                                 related_name='muestreadores',
                                 on_delete=models.CASCADE)
    muestreador = models.ForeignKey(Muestreador,
                                    on_delete=models.CASCADE, related_name="muestreadore")
    observacion = models.TextField(max_length=1500,
                                   blank=True,
                                   null=True)
    laboratorio = models.ForeignKey(Laboratorio,
                                    null=True,
                                    on_delete=models.SET_NULL)
    asignado = models.BooleanField(default=False)
    marca = models.CharField(max_length=100,
                             null=True,
                             blank=True)
    modelo = models.CharField(max_length=100,
                              null=True,
                              blank=True)
    calibracion = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.muestreador.nombre

    @staticmethod
    def returnMuestreadoresBordoPescaCampania(pk_campania):
        trampas_pesca = MuestreadorABordo.objects.filter(campania=pk_campania,
                                                         muestreador__tipo_muestreador__codigo
                                                         = 'TRAMPA')
        pesca = MuestreadorABordo.objects.filter(campania=pk_campania,
                                                 muestreador__tipo_muestreador__codigo
                                                 = 'RED-PESCA')
        list_muestreadores = []
        for muestr in trampas_pesca: list_muestreadores.append(muestr)
        for muestr in pesca: list_muestreadores.append(muestr)
        return list_muestreadores

class Integrantes(models.Model):
    persona = models.ForeignKey(Persona,
                                on_delete=models.CASCADE)
    rol = models.ForeignKey(RolPersona,
                            null=True,
                            on_delete=models.SET_NULL)
    campania = models.ForeignKey(Campania,
                                 related_name='integrantes',
                                 on_delete=models.CASCADE)

    def __unicode__(self):
        return str(self.campania.titulo
                   + ' '
                   + self.persona.nombre
                   + ' '
                   + self.persona.apellido
                   + ' '
                   + self.rol.codigo)

class Etapa(models.Model):
    numero = models.IntegerField()
    fecha_init = models.DateField()
    fecha_fin = models.DateField()
    campania = models.ForeignKey(Campania,
                                 related_name='etapas',
                                 on_delete=models.CASCADE)
    puerto_origen = models.ForeignKey(Puerto,
                                      null=True,
                                      related_name='pto_origen',
                                      on_delete=models.SET_NULL)
    puerto_destino = models.ForeignKey(Puerto,
                                       null=True,
                                       related_name='pto_destino',
                                       on_delete=models.SET_NULL)

    def __str__(self):
        # return 'Inicio:' + str(self.fecha_init) + ' Fin:' + str(self.fecha_fin)
        return str('Nro: "'
               + str(self.numero)
               + '" Fechas:  '\
               + str(self.fecha_init)
               + ' | '
               + str(self.fecha_fin))

class LoginMIC(models.Model):
    ip = models.TextField(max_length=70, blank=True, null=True)
    campania_id = models.IntegerField(blank=True, null=True)

