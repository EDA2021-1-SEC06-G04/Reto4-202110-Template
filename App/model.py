"""
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

from math import sin, cos, sqrt, atan2, radians

import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT.graph import gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
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

    catalog['landing_points'] = mp.newMap(maptype='PROBING', loadfactor=0.5, comparefunction=CompareLandingPoints)
    catalog['cables'] = mp.newMap(loadfactor=4.0)
    catalog['countries'] = mp.newMap(loadfactor=4.0)
    catalog['grafo'] = gr.newGraph(datastructure='ADJ_LIST', directed=True, comparefunction=CompareLandingPoints, size=3300)
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
    



def addCountry_Mapa(catalog, country_agregar):
    countries_mapa = catalog['countries']
    mp.put(countries_mapa, country_agregar['CountryName'], country_agregar)
    gr.insertVertex(catalog['grafo'], country_agregar['CapitalName'])

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
        mp.put(mapa_landing_points, lp_id, lista_vertices)






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


# Funciones de consulta

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



# Funciones de ordenamiento
