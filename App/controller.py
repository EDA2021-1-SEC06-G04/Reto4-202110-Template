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
    loadLP(catalog)
    loadCountries(catalog)


def loadLP(catalog):
    file = cf.data_dir +fileLP
    input_file = csv.DictReader(open(file, encoding="utf-8"),
                                delimiter=",")
    for lp in input_file:
        lp_agregar = {}
        lp_agregar['landing_point'] = lp['landing_point']
        lp_agregar['id'] = lp['id']
        lp_agregar['name'] = lp['name']
        lp_agregar['latitude'] = float(lp['latitude'])
        lp_agregar['longitude'] = float(lp['longitude'])
        model.addLP(catalog, lp_agregar)


def loadCountries(catalog):
    file = cf.data_dir +fileCountries
    input_file = csv.DictReader(open(file, encoding="utf-8"),
                                delimiter=",")
    for country in input_file:
        country_agregar = {}
        country_agregar['CountryName'] = country['CountryName']
        country_agregar['CapitalName'] = country['CapitalName']
        country_agregar['CapitalLatitude'] = float(country['CapitalLatitude'])
        country_agregar['CapitalLongitude'] = float(country['CapitalLongitude'])
        country_agregar['CountryCode'] = float(country['CountryCode'])
        country_agregar['ContinentName'] = float(country['ContinentName'])
        country_agregar['Population'] = int(country['Population'])
        country_agregar['Internet_users'] = int(country['Internet users'])
        model.addCountry(catalog, country_agregar)

#def loadGrafo(catalog):





# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
