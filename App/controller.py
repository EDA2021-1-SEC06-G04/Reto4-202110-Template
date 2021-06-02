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
 """

import config as cf
import model
import csv
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT.graph import gr

fileConnections = 'connections.csv'
fileLP = 'landing_points.csv'
fileCountries = 'countries.csv'

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initCatalog():
    catalog = model.newCatalog()
    return catalog


# Funciones para la carga de datos
def loadData(catalog):
    ultimo_pais = loadCountries(catalog)
    primer_lp = loadLP(catalog)
    for lp in lt.iterator(mp.keySet(catalog['landing_points'])):
        print(lp)
    total_conex_lps = loadConnections(catalog)

    return total_conex_lps, primer_lp, ultimo_pais


def loadLP(catalog):
    file = cf.data_dir + fileLP
    input_file = csv.DictReader(open(file, encoding="utf-8"),
                                delimiter=",")
    primer_lp = None
    contador = 0
    for lp in input_file:
        contador = contador + 1
        lp_agregar = {}
        lp_agregar['landing_point_id'] = lp['landing_point_id']
        lp_agregar['id'] = lp['id']
        lp_agregar['name'] = lp['name']
        lp_agregar['latitude'] = float(lp['latitude'])
        lp_agregar['longitude'] = float(lp['longitude'])
        if contador==1:
            primer_lp = model.addLP_Mapa(catalog, lp_agregar)
        else:
            model.addLP_Mapa(catalog, lp_agregar)

        print(contador)
    return primer_lp

        
        
            


def loadCountries(catalog):
    file = cf.data_dir + fileCountries
    input_file = csv.DictReader(open(file, encoding="utf-8"),
                                delimiter=",")
    for country in input_file:
        
        if not country['CountryName'] == '':
            country_agregar = {}
            country_agregar['CountryName'] = country['CountryName']
            country_agregar['CapitalName'] = country['CapitalName']
            country_agregar['CapitalLatitude'] = float(country['CapitalLatitude'])
            country_agregar['CapitalLongitude'] = float(country['CapitalLongitude'])
            country_agregar['CountryCode'] = country['CountryCode']
            country_agregar['ContinentName'] = country['ContinentName']
            country_agregar['Population'] = int(country['Population'].replace('.',''))
            country_agregar['Internet_users'] = int(country['Internet users'].replace('.',''))
            model.addCountry_Mapa(catalog, country_agregar)
    
    return lt.lastElement(mp.valueSet(catalog['countries']))
    

def loadConnections(catalog):
    file = cf.data_dir + fileConnections
    input_file = csv.DictReader(open(file, encoding="utf-8-sig"),
                                delimiter=",")
    total_conex_lps = 0
    for filacsv in input_file:
        conexion = {'tipo': 'cable'}
        conexion['destiny_lp'] = filacsv['destination']
        conexion['origin_lp'] = filacsv['origin']
        
        if filacsv['cable_length'] == 'n.a.':
            conexion['distance_cable'] = -1
        else:
            conexion['distance_cable'] = float((filacsv['cable_length']).replace(',','').replace(' km',''))
        conexion['capacidad'] = float(filacsv['capacityTBPS'])
        conexion['cable_name'] = filacsv['cable_name']
        conexion['cable_id'] = filacsv['cable_id']
        conexion['cable_owners'] = filacsv['owners']
        model.addConexion(catalog, conexion)
        total_conex_lps = total_conex_lps + 1
    model.conectarVertices_mismoLPs(catalog)
    return total_conex_lps









# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
