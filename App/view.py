"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT.graph import gr
#import folium
#from branca.element import Figure
#import webbrowser
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print('-------------------------------------------------------------------------------------------------------------')
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Consultar la cantidad de clústers en la red y si dos landing points pertenecen al mismo clúster")
    print("3- Consultar los landing points que sirven como interconexión a más cables en la red")
    print("4- Consultar la ruta mínima y su distancia entre País A y País B")
    print("5- Consultar la red de expansión mínima que de cobertura a la mayor cantidad de landing points")
    print("6- Consultar el los países afectados por la falla de un landing point determinado")
    print("7- (BONO) Consultar los países conectados al cable del país con ancho de banda máximo garantizable")
    print("8- (BONO) Consultar ruta mínima en número de saltos para enviar información entre dos direcciones IP")
    print('0- Salir/Exit')
    print('-------------------------------------------------------------------------------------------------------------')


catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:

        print("Cargando información de los archivos ....")
        print('-------------------------------------------------------------------------------------------------------------')
        #Inicializamos el catálogo
        catalog = controller.initCatalog()
        #Cargamos el catálogo
        total_conex_lps, primer_lp, ultimo_pais = controller.loadData(catalog)
        total_lps = mp.size(catalog['landing_points'])
        
        total_paises = mp.size(catalog['countries'])

        print('El total de landing points cargados es {}.'.format(total_lps))
        print('El total de conexiones entre landing points cargadas es {}.'.format(total_conex_lps))
        print('El total de paises cargados es {}.'.format(total_paises))
        
        print('''El primer landing point cargado es {}, con codigo {}
        y sus coordenadas latitud y longitud son: ({}), ({}). '''.format(primer_lp['name'], primer_lp['landing_point_id']
        , primer_lp['latitude'], primer_lp['longitude']))

        print(mp.size(catalog['cables']))
        



    elif int(inputs[0]) == 2:
        print('Ingresa el primer landing point')

    else:
        sys.exit(0)
sys.exit(0)


#def plotstack(cont, path, initialStation, destStation):
    #fig = Figure(height=350, width=550)
    #my_map = folium.Map(location=[1.29,103.85])
    #fig.add_child(my_map)

    #name = initialStation.split('-')[0]
    #base_cords, base_road, base_descr = controller.getCoords(cont, name)

    #folium.Marker(location = base_cords, popup?'Estación inicial').add_to(my_map)

    #feat = folium.FeatureGroup('Route from {} to {}'.format(initialStation, destStation))

    #all_coords = [base_coords]
    #while (not stack.isEmpty(path)):
    #    stop = stack.pop(path)
    #    w = stop['weight']
    #    if w>0:
    #        vB = stop['vertexB']
    #        new_coords, new_road, new_descr = controller.getCoords(cont, vB, split('-')[0])
    #        folium.Marker(location=new_coords, popup = new_road+'\n'+new_descr).add_to(my_map)

    #        all_coords.append(new_coords)
    
    #line = folium.vector_layers.PolyLine(all_coords, popup='Route from {} to{}'.format(initialStation, destStation))add_to(feat)

    #feat.add_to(my_map)
    #folium.LayerControl().add_to(my_map)
    #my_map.save('Mi_mapa.html')
    #webbrowser.open('Mi_mapa.html')

