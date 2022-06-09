import decimal
import math
import time
import numpy as np
from datetime import timedelta
from operaciones.oDetalles.pesca.models import DetalleRedArrastre
from operaciones.oPesca.captura.models import Captura

class EstadisticaPesquera:
    """
        Esta es la clase que va a tener todos los metodos para realizar el
        calculo estadistico de una campaña.
    """
    @staticmethod
    def distanciaVelocidadPorTiempoArrastre(hora_inicial,
                                            hora_final,
                                            velocidad_arrastre):
        pass
        """
        :param hora_inicial: datetime.time
        :param hora_final: datetime.time
        :param velocidad_arrastre: integer
        :return: Calcula la distancia con la velocidad por tiempo de arrastr
        """
    @staticmethod
    def KgHporEspecie(operacion, kg_especie):
        fecha_init = operacion.inicio_espacio_temporal.fecha_hora
        fecha_fin = operacion.fin_espacio_temporal.fecha_hora
        if fecha_init >= fecha_fin:
            return None
        else:
            # Calculo de tiempo por medio de deltatime objects
            delta_inicial = timedelta(hours=fecha_init.hour,
                                      minutes=fecha_init.minute,
                                      seconds=fecha_init.second)
            delta_final = timedelta(hours=fecha_fin.hour,
                                    minutes=fecha_fin.minute,
                                    seconds=fecha_fin.second)
            delta_resultado = delta_final - delta_inicial
            # Tiempo de arrastre en hr
            tiempo_arrastre = delta_resultado.seconds / 3600
            return float(kg_especie) / tiempo_arrastre

    @staticmethod
    def porcentajeJuveniles(muestra, talla_juv):
        """
        :param muestra: Muestra Object
        :param talla_juv: talla donde comienzan lso juveniles
        :return:la suma de todas las cantidades que cumplen con la talla
        menor a la talla de juveniles
        """
        total = 0
        cantidad = 0
        detalles = muestra.getDetallesXMuestra()
        if detalles:
            for detalle in detalles:
                if detalle.cant_hembra:
                    hembras = detalle.cant_hembra
                else:
                    hembras = 0
                if detalle.cant_macho:
                    machos = detalle.cant_macho
                else:
                    machos = 0
                if detalle.cant_indet:
                    indt = detalle.cant_indet
                else:
                    indt = 0
                if detalle.talla < talla_juv:
                    cantidad = cantidad + hembras + machos + indt
                total = total + hembras + machos + indt
            return (float(cantidad) * 100) / float(total)
        return total

    @staticmethod
    def tallaMediaxCaptura(muestra):
        """
        Esta funcion calcula el promedio de talla para una muestra
        :param muestra: muestra object
        :return: promedio de talla acumulado
        """
        detalles = muestra.getDetallesXMuestra()
        if detalles:
            cant_total_ejemplares = 0
            suma_acumulada_talla = 0
            for detalle in detalles:
                machos = hembras = indt = 0
                if detalle.cant_macho: machos = detalle.cant_macho
                if detalle.cant_hembra: hembras = detalle.cant_hembra
                if detalle.cant_indet: indt = detalle.cant_indet
                ejemplares_en_detalle = machos + hembras + indt
                cant_total_ejemplares = (cant_total_ejemplares
                                         + ejemplares_en_detalle)
                suma_acumulada_talla = (suma_acumulada_talla
                                        + (detalle.talla
                                           * ejemplares_en_detalle))
            tallaMedia = (float(suma_acumulada_talla)
                          / float(cant_total_ejemplares))
            return tallaMedia
        return None

    @staticmethod
    def toneladamillanautica2(area_barrida, captura_kg):
        if area_barrida and captura_kg:
            return (float(captura_kg) / 1000) / float(area_barrida)
        return None

    @staticmethod
    def milesIndividuosMillaNautica2(captura_kg,
                                     ejemplares_en_kg,
                                     area_barrida):
        if captura_kg and ejemplares_en_kg and area_barrida:
            nroEjemplares = captura_kg * ejemplares_en_kg
            milesIndv = ((float(nroEjemplares) / 1000) / float(area_barrida))
            return milesIndv
        return None

    @staticmethod
    def biomasaXespecieDeCampania(campania,
                                  especie):
        """
        :param campania:
        :param especie:
        1) Por cada estrato de la campaña tengo que filtrar las capturas de cada uno.
        2) Con esa lista filtrada construyo diccionarios por cada captura con su nro lance y densidad.
        3) Hago los calculos necesarios por cada estrato
        4) Agrego como dict el paso 3 a una lista de resultados de todos los estratos.
        5) Hago un calculo de resultados totales con la lista de resultados de estratos
        6) Retorno esa lista.
        """
        results_estratos = []
        for estrato in campania.estratos.all().order_by('numero'):
            dict_results_estrato = {}
            capturas_estrato = Captura.getCapturaxEstrato(estrato)
            nro_lances_list = []
            [
                nro_lances_list.append(captura.nro_lance)
                for captura in capturas_estrato
                if captura.nro_lance not in nro_lances_list
                ]
            lances_densidad_list = []
            for nro_lance in nro_lances_list:
                lance_dict = {}
                lance_dict['nro_lance'] = nro_lance
                lance_dict['densidad'] = 0
                captura_especie = None
                for captura in capturas_estrato:
                    if (nro_lance == captura.nro_lance
                        and especie == captura.especie):
                        captura_especie = captura
                if captura_especie:
                    # seteo el dict de lance con la densidad
                    # consulto directamente con el tipo detalleRedArrastre
                    detalle_op = Captura.getDetalleOperacion(captura_especie)
                    kg = captura_especie.kg
                    if isinstance(detalle_op, DetalleRedArrastre):
                        if detalle_op.area_barrida:
                            area_barrida = detalle_op.area_barrida
                            lance_dict['densidad'] = EstadisticaPesquera.toneladamillanautica2(area_barrida,
                                                                                               kg)
                lances_densidad_list.append(lance_dict)
            if lances_densidad_list:
                """
                Calculos realizados por estrato:
                * densidad_media = SUM(de todas las densidades) / Total de lances
                * densidad area = densidad_media * area_estrato
                * varianza dens. = var(densidades) * count(densidades) / count(densidad) - 1
                * promedio de la varianza
                * BIOMASA: densidad_media * area_estrato
                * varianza biomasa = varianza * area*area
                * desviacion biomasa: raiz_cuadrada(varianza_bioamasa)
                * Intervalo de confianza: 2.23 * desviacion_biomasa
                *
                """
                dict_results_estrato['estrato'] = estrato
                dict_results_estrato['lances'] = lances_densidad_list
                array_densidad = []
                for lance in lances_densidad_list:
                    array_densidad.append(lance['densidad'])
                np_array_densidades = np.array(array_densidad)
                densidad_media = np_array_densidades.sum() / len(np_array_densidades)
                densidad_area = densidad_media * estrato.area
                varianza_dens = (np_array_densidades.var()
                                 * len(np_array_densidades)
                                 / (len(np_array_densidades)-1))
                varianza_media = varianza_dens / len(np_array_densidades)
                biomasa = densidad_area
                var_biomasa = varianza_media * (estrato.area * estrato.area)
                desv_biomasa = math.sqrt(var_biomasa)
                intervalo_confianza = 2.23 * desv_biomasa
                dict_results_estrato['densidad_media'] = densidad_media
                dict_results_estrato['densidad_area'] = densidad_area
                dict_results_estrato['varianza_dens'] = varianza_dens
                dict_results_estrato['varianza_media'] = varianza_media
                dict_results_estrato['biomasa'] = biomasa
                dict_results_estrato['var_biomasa'] = var_biomasa
                dict_results_estrato['desv_biomasa'] = desv_biomasa
                dict_results_estrato['intervalo_confianza'] = intervalo_confianza
                results_estratos.append(dict_results_estrato)
        if results_estratos:
            """
            Aca hago los calculos totales de todos los resultados
            * Suma de area de densidades
            * Dens. Med Total
            * Cant de estratos
            * Biomasa Total
            * Var. Biom. Total
            """
            suma_areas = 0
            suma_areas_estrato = 0
            biomasa_total = 0
            vari_biomasa_total = 0
            for dict_result in results_estratos:
                suma_areas += float(dict_result['densidad_area'])
                suma_areas_estrato += float(dict_result['estrato'].area)
                biomasa_total += float(dict_result['biomasa'])
                vari_biomasa_total += float(dict_result['var_biomasa'])
            densidades_medias = suma_areas / suma_areas_estrato
            cant_estratos = len(campania.estratos.all())
            desviacion_biomasa = math.sqrt(vari_biomasa_total)
            semiran_int_confianza = 2.2*desviacion_biomasa
            resultados_globales = {}
            resultados_globales['resultados_estratos'] = results_estratos
            resultados_globales['suma_areas'] = suma_areas
            resultados_globales['densidad_media_total'] = densidades_medias
            resultados_globales['cant_estratos'] = cant_estratos
            resultados_globales['biomasa_total'] = biomasa_total
            resultados_globales['varianza_biomasa_total'] = vari_biomasa_total
            resultados_globales['semiran_int_confianza'] = semiran_int_confianza
            return resultados_globales
        return None


    @staticmethod
    def ponderacionTallasEspecie(dict_estratos):
        """
        ESta def calcula la ponderacion de tallas de una unica especie por estrato
        Aplica todos los calculos necesarios
        :param dict_estratos: Diccionario con los valores de la campaña por estrato.
        :format dict_estratos:
        dict = {
            estratos: [{
                numero: int
                area: int
                estaciones: [{
                     nro_estacion_barco: int
                     fecha: date
                     lat: float
                     lon: float
                     lances: [{
                         numero: int
                         captura_kg: float
                         area: float
                         peso_capt: float
                         peso_muestra: float
                         detalles: [{
                            machos: int
                            hemb: int
                            ind: int
                            cant_totales: int
                            }]
                     }]
                }]
        }
        :return: un dict con los resultados:
        """
        dict_estratos = EstadisticaPesquera.ponderacionTallasCleanDict(dict_estratos)
        # Ahora tengo que calcular la ponderacion por cada muestra
        # teniendo en cuenta que ya tengo las partes para hacer los calculos necesarios
        resultados_dict = {}
        resultados_array = []
        suma_ponderaciones_talla = []
        ponderacion_total = 0
        for estrato_dict in dict_estratos['estratos']:
            dict_rest_estrato = {}
            lances_list = []
            suma_ponderacion_estrato = []
            # Si el estrato ni tiene estaciones que continue con el bucle
            if not estrato_dict['estaciones']:
                continue
            for estacion in estrato_dict['estaciones']:
                for lance_dict in estacion['lances']:
                    if not estrato_dict['factor_ponderacion_biomasa']:
                        continue
                    factor_pond = decimal.Decimal(estrato_dict['factor_ponderacion_biomasa'])
                    factor_muestra = decimal.Decimal(lance_dict['factor_muestra'])
                    ponderacion = (factor_muestra * factor_pond)
                    dict_rest_lance = {}
                    dict_rest_lance['lance'] = lance_dict['numero']
                    dict_rest_lance['nro_estacion'] = estacion['nro_estacion_barco']
                    dict_rest_lance['fecha'] = lance_dict['fecha']
                    dict_rest_lance['captura_kg'] = lance_dict['captura_kg']
                    detalles_list = []
                    suma_ponderacion_lance = 0
                    for detalle in lance_dict['detalles']:
                        detalle_dict = {}
                        detalle_dict['talla'] = detalle['talla']
                        detalle_dict['machos'] = detalle['machos']
                        detalle_dict['hembras'] = detalle['hembras']
                        detalle_dict['cant_totales'] = detalle['cant_totales']
                        detalle_dict['indeterminados'] = detalle['indeterminados']
                        total = detalle['machos'] + detalle['hembras'] + detalle['cant_totales'] + detalle['indeterminados']
                        if total == 0:
                            continue
                        else:
                            res_pon = total * ponderacion
                            detalle_dict['res_pon'] = res_pon
                            talla = detalle['talla']
                            suma_ponderacion_estrato = complete_dict_talla(
                                                           suma_ponderacion_estrato,
                                                           talla,
                                                           res_pon, total)
                            suma_ponderaciones_talla = complete_dict_talla(
                                                            suma_ponderaciones_talla,
                                                            talla,
                                                            res_pon, total)
                            ponderacion_total += res_pon
                            detalles_list.append(detalle_dict)
                            suma_ponderacion_lance += res_pon
                    dict_rest_lance['suma_ponderacion_lance'] = suma_ponderacion_lance
                    dict_rest_lance['detalles'] = detalles_list
                    lances_list.append(dict_rest_lance)
            suma_ponderacion_estrato = sorted(suma_ponderacion_estrato,
                                              key=lambda k: k['talla'])
            dict_rest_estrato['suma_ponderacion_talla'] = suma_ponderacion_estrato
            dict_rest_estrato['lances'] = lances_list
            dict_rest_estrato['estrato'] = estrato_dict['numero']
            dict_rest_estrato['suma_capturas_estrato'] = estrato_dict['suma_capturas_estrato']
            factor_ponderacion_biomasa = decimal.Decimal(
                estrato_dict['factor_ponderacion_biomasa'])
            dict_rest_estrato['factor_ponderacion_biomasa'] = factor_ponderacion_biomasa
            dict_rest_estrato['factor_ponderacion'] = ponderacion
            dict_rest_estrato['biomasa'] = estrato_dict['biomasa']
            resultados_array.append(dict_rest_estrato)
        resultados_dict['estratos'] = resultados_array
        suma_pond_ordenada = sorted(suma_ponderaciones_talla,
                                    key=lambda k: k['talla'])
        resultados_dict['suma_ponderaciones_talla'] = suma_pond_ordenada
        resultados_dict['ponderacion_total'] = ponderacion_total
        return resultados_dict

    @staticmethod
    def ponderacionTallasCleanDict(dict_estratos):
        # Primero calculo la biomasa de todos los estratos y lances
        # Necesito hacer el calculo de densidad por lance para depsues calcular la biomasa
        # Sumar las biomasas y asi poder hacer los calculos de abundancia
        if 'estratos' in dict_estratos:
            estratos = []
            biomasa_total = 0
            suma_capturas_estrato = 0
            for estrato_dict in dict_estratos['estratos']:
                densidades_estrato = []
                if 'estaciones' in estrato_dict:
                    suma_capturas_estrato = 0
                    for estacion in estrato_dict['estaciones']:
                        if 'lances' in estacion:
                            if estacion['lances']:
                                for lance_dict in estacion['lances']:
                                    if not 'area' in lance_dict:
                                        # Si no tiene area el lance, sigo con la ejecucion del bucle
                                        # Y no se tiene en cuenta este lance
                                        continue
                                    if not lance_dict['area']:
                                        continue
                                    else:
                                        densidad = EstadisticaPesquera \
                                            .toneladamillanautica2(lance_dict['area'],
                                                                   lance_dict['captura_kg'])
                                        lance_dict['densidad'] = densidad
                                        captura_kg = lance_dict['captura_kg']
                                        if 'peso_muestra' in lance_dict:
                                            factor_muestra = (lance_dict['captura_kg']
                                                              / lance_dict['peso_muestra'])
                                            lance_dict['factor_muestra'] = factor_muestra
                                        # Si no tiene cargado el peso de la muestra, sigo con
                                        # la ejecucion
                                        else:
                                            lance_dict['factor_muestra'] = None
                                            continue
                                        suma_capturas_estrato += lance_dict['captura_kg']
                                        densidades_estrato.append(round(densidad, 2))
                np_array_densidades = np.array(densidades_estrato)
                cant_lances = estrato_dict['cant_lances']
                suma_densidades_capturas = estrato_dict["suma_densidades_capturas"]
                densidad_media_estrato = round(( suma_densidades_capturas/cant_lances),3) if cant_lances != 0 else suma_densidades_capturas
                biomasa = (densidad_media_estrato * estrato_dict['area'])
                area_estrato = estrato_dict['area']
                estrato_dict['biomasa'] = biomasa
                biomasa_total += biomasa
                estrato_dict['suma_capturas_estrato'] = suma_capturas_estrato
                # Factor de ponderacion: Biomasa Estrato / Suma capturas en el estrato
                if(suma_capturas_estrato > 0):
                    factor_ponderacion_biomasa = decimal.Decimal(biomasa) / suma_capturas_estrato
                else:
                    factor_ponderacion_biomasa = float("nan")
                estrato_dict['factor_ponderacion_biomasa'] = factor_ponderacion_biomasa
                estratos.append(estrato_dict)
        return dict_estratos



def complete_dict_talla(array_tallas, talla, value, cantidad):
    if not array_tallas:
        dict_talla = {
            "talla": talla,
            "suma_ponderacion": value,
            "cantidad": cantidad
        }
        array_tallas.append(dict_talla)
    else:
        if not any(d['talla'] == talla
                   for d in array_tallas):
            dict_talla = {
                "talla": talla,
                "suma_ponderacion": value,
                "cantidad": cantidad,
            }
            array_tallas.append(dict_talla)
        else:
            for dict_tallas in array_tallas:
                if dict_tallas['talla'] == talla:
                    pond = decimal.Decimal(dict_tallas['suma_ponderacion'])
                    pond += value
                    dict_tallas['suma_ponderacion'] = pond
                    dict_tallas['cantidad'] += cantidad
    return array_tallas