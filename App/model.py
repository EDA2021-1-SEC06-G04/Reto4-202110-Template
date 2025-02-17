﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

from DISClib.DataStructures.edge import weight
from DISClib.ADT.indexminpq import contains, size
from DISClib.ADT.orderedmap import newMap
from math import sin, cos, sqrt, atan2, radians

import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT import orderedmap as om
from DISClib.ADT.graph import gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.ADT import queue as qu
from DISClib.Algorithms.Graphs import prim
from DISClib.ADT import stack as stk

assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    catalog = {
        'landing_points': None,
        'countries': None,
        'grafo': None
    }
    #llaves son landing_point__id, valores son toda la info del lp
    catalog['landing_points'] = mp.newMap(maptype='PROBING', loadfactor=0.5, comparefunction=CompareLandingPoints)
    #llaves son nombres de lp, valores son los landing_point_id para acceder al mapa de arriba
    catalog['landing_points2'] = mp.newMap(maptype='PROBING', loadfactor=0.5, comparefunction=CompareLandingPoints)
    #llaves son ['cable_name'] valores son toda la info del cable del archivo de conexiones
    catalog['cables'] = mp.newMap(loadfactor=4.0)
    #llaves son nombres de paises, valores son toda la info del pais
    catalog['countries'] = mp.newMap(loadfactor=4.0)
    #llaves son nombres de capitales, valores son los nombres de paises para acceder al mapa de arriba
    catalog['countries2'] = mp.newMap(loadfactor=4.0)
    #grafo : vertices: lp-cables y capitales, arcos:conexiones por cable y conexiones terrestres con capitales (y 
# conexiones triviales entre vertices del mismo lp)
    catalog['grafo'] = gr.newGraph(datastructure='ADJ_LIST', directed=True, comparefunction=CompareLandingPoints, size=2800)
    #aqui se guardara la info general que retorna el algoritmmo de Kosaraju sobre el grafo
    catalog['Kosaraju'] = None
    catalog['MST'] = None
    return catalog

# Funciones para agregar informacion al catalogo
def addLP_Mapa(catalog, lp_agregar):
    mapa_landing_points = catalog['landing_points']
    lp_agregar['lista_vertices'] = lt.newList('ARRAY_LIST')
    if ', ' in lp_agregar['name']:
        lp_agregar['country'] = lp_agregar['name'].split(', ')[-1]
    else:
        lp_agregar['country'] = lp_agregar['name']
    mp.put(mapa_landing_points, lp_agregar['landing_point_id'], lp_agregar)

    mapa_landing_points2 = catalog['landing_points2']
    mp.put(mapa_landing_points2, lp_agregar['name'], lp_agregar['landing_point_id'])
    return lp_agregar
    



def addCountry_Mapa(catalog, country_agregar):
    countries_mapa = catalog['countries']
    mp.put(countries_mapa, country_agregar['CountryName'], country_agregar)
    gr.insertVertex(catalog['grafo'], country_agregar['CapitalName'])
    countries_mapa2 = catalog['countries2']
    mp.put(countries_mapa2, country_agregar['CapitalName'], country_agregar['CountryName'])


def addConexion(catalog, conexion):
    cable = conexion['cable_id']
    o_lp = conexion['origin_lp']
    d_lp = conexion['destiny_lp']
    v_origen = o_lp + '-' + cable
    v_destino = d_lp + '-' + cable
    addLP_graph(catalog, o_lp, cable)
    addLP_graph(catalog, d_lp, cable)
    addVertice_a_lista_vertices_de_LP(catalog, o_lp, cable)
    addVertice_a_lista_vertices_de_LP(catalog, d_lp, cable)
    distancia = calcularDistancia(catalog, o_lp, d_lp)
    addConexion_graph(catalog, v_origen, v_destino, distancia)
    addCable_Mapa(catalog, conexion)

def addCable_Mapa(catalog, conexion):
    mapa_cables = catalog['cables']
    nombre_cable = conexion['cable_name']
    id_cable = conexion['cable_id']
    propietarios = conexion['cable_owners']
    largo_cable= conexion['distance_cable']
    lp1 = conexion['destiny_lp']
    lp2 = conexion['origin_lp']

    entry = mp.get(mapa_cables, nombre_cable)
    if entry is not None:
        cable = me.getValue(entry)
        lista_lps = cable['lista_lps']
        if not lt.isPresent(lista_lps, lp1):
            lt.addLast(lista_lps, lp1)
        if not lt.isPresent(lista_lps, lp2):
            lt.addLast(lista_lps, lp2)
    else:
        cable = {}
        cable['nombre_cable'] = nombre_cable
        cable['id_cable'] = id_cable
        cable['propietarios'] = propietarios
        cable['largo_cable'] = largo_cable
        cable['lista_lps'] = lt.newList('ARRAY_LIST')
        lt.addLast(cable['lista_lps'], lp1)
        lt.addLast(cable['lista_lps'], lp2)
        mp.put(mapa_cables, nombre_cable, cable)




def calcularDistancia(catalog, lp_1, lp_2):
    #la forma de usar esta funcion es que para lp1 siempre se debe ingresar un landing point,
    # para lp2 se puede ingresar un pais y se le obtendran las coordenadas del mapa_paises
    mapa_lps = catalog['landing_points']
    mapa_paises = catalog['countries']
    
    lp_1 =  me.getValue(mp.get(mapa_lps, lp_1))
    lat1, lon1 = lp_1['latitude'], lp_1['longitude']
    if mp.contains(mapa_lps, lp_2):
        lp_2 = me.getValue(mp.get(mapa_lps, lp_2))
        lat2, lon2 = lp_2['latitude'], lp_2['longitude']
    elif mp.contains(mapa_paises, lp_2):
        #lp_2 en realidad es un nombre de un pais
        lp_2 = me.getValue(mp.get(mapa_paises, lp_2))
        lat2, lon2 = lp_2['CapitalLatitude'], lp_2['CapitalLongitude']


    R = 6373.0

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance


def addLP_graph(catalog, lp, cable):
    mapa_lps = catalog['landing_points']
    mapa_paises = catalog['countries']
    lp_cable = lp + '-' + cable
    grafo = catalog['grafo']
    if not gr.containsVertex(grafo, lp_cable):
        gr.insertVertex(grafo, lp_cable)

    #de aqui en adelante lo que se hace es conectar este vertice con la capital de su pais
#    print(lp, mp.contains(mapa_lps, lp))
    pais = me.getValue(mp.get(mapa_lps, lp))['country']
    capital = me.getValue(mp.get(mapa_paises, pais))['CapitalName']
    distancia = calcularDistancia(catalog, lp, pais)

    addConexion_graph(catalog, lp_cable, capital, distancia)
    addConexion_graph(catalog, capital, lp_cable, distancia)

def addConexion_graph(catalog, vertice_origen, vertice_destino, distancia):
    origen = vertice_origen
    destino = vertice_destino
    grafo = catalog['grafo']
    edge = gr.getEdge(grafo, origen, destino)
    if edge is None:
        gr.addEdge(grafo, origen, destino, distancia)

    
def addVertice_a_lista_vertices_de_LP(catalog, lp_id, cable):
    mapa_landing_points = catalog['landing_points']
    entry_lista_vertices = mp.get(mapa_landing_points, lp_id)

    vertice = lp_id + '-' + cable

    if entry_lista_vertices is not None:
        lista_vertices = me.getValue(entry_lista_vertices)['lista_vertices']
        if not lt.isPresent(lista_vertices, vertice):
            lt.addLast(lista_vertices, vertice)
    else:
        lista_vertices = lt.newList('ARRAY_LIST')
        lt.addLast(lista_vertices, vertice)
        mp.put(mapa_landing_points, lp_id, {'lista_vertices':lista_vertices})






# Funciones para creacion de datos

def conectarVertices_mismoLPs(catalog):
    mapa_LPs = catalog['landing_points']
    lista_LPs = mp.keySet(mapa_LPs)
    for lp in lt.iterator(lista_LPs):
        lstVertices = me.getValue(mp.get(mapa_LPs, lp))['lista_vertices']
        prevVertice = None

        for vertice in lt.iterator(lstVertices):
            if prevVertice is not None:
                addConexion_graph(catalog, prevVertice, vertice, 0)
                addConexion_graph(catalog, vertice, prevVertice, 0)
            prevVertice = vertice


def ejecutar_Kosaraju(catalog):
    grafo = catalog['grafo']
    resultado_kosaraju = scc.KosarajuSCC(grafo)
    catalog['Kosaraju'] = resultado_kosaraju
    return resultado_kosaraju

# Funciones de consulta

def Calcular_clusters(catalog):
    info_kosaraju = catalog['Kosaraju']
    cantidad = scc.connectedComponents(info_kosaraju)
    return cantidad


def lp_Fuertemente_conectados(catalog, landing_point1_nombre, landing_point2_nombre):
    mapa_lps = catalog['landing_points']
    mapa_lps2 = catalog['landing_points2']
    landing_point1 = me.getValue(mp.get(mapa_lps2, landing_point1_nombre))
    landing_point2 = me.getValue(mp.get(mapa_lps2, landing_point2_nombre))
    #creo que no toca coger la lista y chequear todos, solo basta con uno de cada uno
    listas_vertices_1 = me.getValue(mp.get(mapa_lps, landing_point1))['lista_vertices']
    listas_vertices_2 = me.getValue(mp.get(mapa_lps, landing_point2))['lista_vertices']
    respuesta = False
    for vertice1 in lt.iterator(listas_vertices_1):
        for vertice2 in lt.iterator(listas_vertices_2):
            if vertices_Fuertemente_conectados(catalog, vertice1, vertice2):
                respuesta = True
                break
    return respuesta


def vertices_Fuertemente_conectados(catalog, vertice1, vertice2):
    info_kosaraju = catalog['Kosaraju']
    f_conectados = scc.stronglyConnected(info_kosaraju, vertice1, vertice2)
    return f_conectados


# ----------------------------------------------------- REQ 2 ----------------------------------------------------- #
def lpInterconexion(catalog):
    mapa_grande = catalog['landing_points']
    rbt_nuevo = om.newMap(omaptype='RBT', comparefunction=CompareIntegersOM)
#    total = 0

    for lp in lt.iterator(mp.valueSet(mapa_grande)):
        lista_vertices = lp['lista_vertices']
        cant_vertices = lt.size(lista_vertices)
#        total = total + cant_vertices
        if not om.contains(rbt_nuevo, cant_vertices):
            lista_lps = lt.newList(datastructure='ARRAY_LIST')
            lt.addLast(lista_lps, (lp, lista_vertices))
            om.put(rbt_nuevo, cant_vertices, lista_lps)
        else:
            lista_lps = me.getValue(om.get(rbt_nuevo, cant_vertices))
            lt.addLast(lista_lps, (lp, lista_vertices))

    return rbt_nuevo
    

# ----------------------------------------------------- REQ 3 ----------------------------------------------------- #
def RutaMinima(catalog, paisA, paisB):
    mapaLP = catalog['landing_points']
    mapaCountries = catalog['countries']
    mapaCountries2 = catalog['countries2']
    grafo = catalog['grafo']

    capitalA = me.getValue(mp.get(mapaCountries, paisA))['CapitalName']
    capitalB = me.getValue(mp.get(mapaCountries, paisB))['CapitalName']
    
    dijkstra = djk.Dijkstra(grafo, capitalA)

    distancia_total = djk.distTo(dijkstra, capitalB)
    ruta_cruda = djk.pathTo(dijkstra, capitalB)
    ruta = qu.newQueue('ARRAY_LIST')
    previo = None
    while not stk.isEmpty(ruta_cruda):
        punto = stk.pop(ruta_cruda)['vertexB']
        dist = djk.distTo(dijkstra, punto)
        if not mp.contains(mapaCountries2, punto):
            punto = 'Landing point ' + punto.split('-')[0]
        print(dist)
        print(punto)
        p_d = (punto, dist)
        if not previo == punto:
            qu.enqueue(ruta, p_d)
        previo = punto


    return ruta, distancia_total

# ----------------------------------------------------- REQ 4 ----------------------------------------------------- #
def MST(catalog):
    grafo = catalog['grafo']
    mst = prim.PrimMST(grafo)
    catalog['MST'] = mst
    return mst

def tot_peso_mst(grafo, mst):
    return prim.weightMST(grafo, mst)


def num_vert_mst(mst):
    grafo = mst['grafo']
    return gr.numVertices(grafo)

def max_rama(mst):
    grafo = mst['grafo']
    max_rama = 0
    for vertice1 in lt.iterator(gr.vertices(grafo)):
        dijsktra = djk.initSearch(grafo, vertice1)
     #   print('iniciando dijsktra para el vertice {}'.format(vertice1))
        for vertice2 in lt.iterator(gr.vertices(grafo)):
     #       print('revisando camino hacia el vertice {}'.format(vertice2))
            if not vertice1 == vertice2:
                if djk.hasPathTo(dijsktra, vertice2):
                  #  print('el vertice {} tiene camino'.format(vertice2))
                    rama = djk.distTo(dijsktra, vertice2)
                   # print(rama)
                    if rama > max_rama:
                        max_rama = rama
    return max_rama

def graphPrim(mst):
    '''for vertice in lt.iterator(mp.keySet(mst['edgeTo'])):
        print(vertice)
        edgeTo = me.getValue(mp.get(mst['edgeTo'], vertice))
        print(edgeTo)'''
    grafo = gr.newGraph(datastructure='ADJ_LIST', directed=True, comparefunction=CompareLandingPoints, size=2300)
    
    for conexion in lt.iterator(mp.valueSet(mst['edgeTo'])):
        vertexA = conexion['vertexA']
        vertexB = conexion['vertexB']
        weight = conexion['weight']
        gr.insertVertex(grafo, vertexA)
        gr.insertVertex(grafo, vertexB)
        gr.addEdge(grafo, vertexA, vertexB, weight)
    
    mst['grafo'] = grafo
#    print('AQUI ',lt.size(gr.edges(grafo)))
#    print('AQUI: ', lt.size(gr.vertices(grafo)))
    return grafo

    




# ----------------------------------------------------- REQ 5 ----------------------------------------------------- #
def fallasLP(catalog, lp):
    mapaLP2 = catalog['landing_points2']
    mapaLP = catalog['landing_points']
    countries = catalog['countries2']
    grafo = catalog['grafo']
    id_lp = me.getValue(mp.get(mapaLP2, lp))
    lista_vertices = me.getValue(mp.get(mapaLP,id_lp))['lista_vertices']

    mpRespuesta = mp.newMap(loadfactor=4.0)
    for vertice in lt.iterator(lista_vertices):
        lt_adj = gr.adjacents(grafo, vertice)
        for adj in lt.iterator(lt_adj):
            if mp.contains(countries, adj):
                pais = me.getValue(mp.get(countries, adj))
                distancia = calcularDistancia(catalog, id_lp,pais)
            else:
                adj_lp_id = adj.split('-')[0]
                pais_crudo = me.getValue(mp.get(mapaLP, adj_lp_id))['name']
                pais = pais_crudo.split(', ')[-1]
                distancia = calcularDistancia(catalog, id_lp, adj_lp_id)
            mp.put(mpRespuesta, pais, (pais, distancia))

    return mpRespuesta
            


# Funciones utilizadas para comparar elementos dentro de una lista

def CompareLandingPoints(landing_point, keyLP):
    """
    Compara dos landing points
    """
    LPcode = keyLP['key']
    if (landing_point == LPcode):
        return 0
    elif (landing_point > LPcode):
        return 1
    else:
        return -1

def CompareIntegersOM(int1, int2):
    """
    Compara dos landing points
    """
#    int2 = int2['key']
    if (int1 == int2):
        return 0
    elif (int1 < int2):
        return 1
    else:
        return -1


# Funciones de ordenamiento
