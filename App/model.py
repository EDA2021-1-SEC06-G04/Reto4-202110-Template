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
        'grafo_cables': None
    }

    catalog['landing_points'] = mp.newMap(maptype='PROBING', loadfactor=0.5)
    catalog['countries'] = mp.newMap(loadfactor=4.0)
    catalog['grafo_cables'] = gr.newGraph(datastructure='ADJ_LIST', directed=True, comparefunction=CompareLandingPoints)



# Funciones para agregar informacion al catalogo
def addLP(catalog, lp_agregar):
    landing_points_mapa = catalog['landing_points']
    mp.put(landing_points_mapa, lp_agregar['landing_point'], lp_agregar)


def addCountry(catalog, country_agregar):
    countries_mapa = catalog['countries']
    mp.put(countries_mapa, country_agregar['CountryName'], country_agregar)



# Funciones para creacion de datos

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
