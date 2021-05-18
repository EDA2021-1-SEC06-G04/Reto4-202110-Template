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
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Consultar la cantidad de clústers en la red y si dos landing points pertenecen al mismo clúster")
    print("3- Consultar los landing points que sirven como interconexión a más cables en la red")
    print("4- Consultar la ruta mínima y su distancia entre País A y País B")
    print("5- Consultar la red de expansión mínima que de cobertura a la mayor cantidad de landing points")
    print("6- Consultar el los países afectados por la falla de un landing point determinado")
    print("7- (BONO) Consultar los países conectados al cable del país con ancho de banda máximo garantizable")
    print("8- (BONO) Consultar ruta mínima en número de saltos para enviar información entre dos direcciones IP")


catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        #Inicializamos el catálogo
        catalog = controller.initCatalog()
        #Cargamos el catálogo
        controller.loadData(catalog)



    elif int(inputs[0]) == 2:
        pass

    else:
        sys.exit(0)
sys.exit(0)
