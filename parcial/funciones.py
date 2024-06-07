# 1) Cargar archivo: Se pedirá el nombre del archivo y se cargarán en una lista los elementos
# del mismo.
# 2) Imprimir lista: Se imprimirá por pantalla la tabla (en forma de columnas) con los datos de los
# servicios.
# 3) Asignar totales: Se deberá hacer uso de una función lambda que asignará a cada servicio el
# total calculado (totalServicio) de la siguiente forma: cantidad x precioUnitario.
# 4) Filtrar por tipo: Se deberá generar un archivo igual al original, pero donde solo aparezcan
# servicios del tipo seleccionado.
# 5) Mostrar servicios: Se deberá mostrar por pantalla un listado de los servicios ordenados por
# descripción de manera ascendente.
#6) Guardar servicios: Se deberá guardar el listado del punto anterior en un archivo de tipo json.
# 7) Salir.
import json
def menu():
    print("\n--- Menú ---\n"
        "1. Cargar archivo\n"
        "2. Imprimir lista\n"
        "3. Asignar totales\n"
        "4. Filtrar por tipo\n"
        "5. Mostrar servicios\n"
        "6. Guardar servicios\n"
        "7. Salir\n")

def cargar_archivo(file:str)->list:
    """Esta funcion se encarga de cargar el archivo

    Args:
        file (str): ruta del archivo json

    Returns:
        list: _description_
    """
    with open(file, 'r') as archivo:
        datos = json.load(archivo)

    return datos

def imprimir_lista(lista:list):
    """Imprime la lista del archivo

    Args:
        lista (list): lista de los servicios
    """
    print('-' * 54)

    for servicio in lista:
        print(f"| {servicio['id_servicio']:3}|"
              f" {servicio['descripcion']:23}|"
              f" {servicio['tipo']:2}|"
              f" {servicio['precioUnitario']:7}|"
              f" {servicio['cantidad']:4}|"
              f" {servicio['totalServicio']:2}|")

def asignar_totales(servicios:list)->list:
    """ asignará a cada servicio el total calculado

    Args:
        servicios (list): lista de los servicios

    Returns:
        list:
    """
    calcular_total = lambda servicio: float(servicio['cantidad']) * float(servicio["precioUnitario"])

    for servicio in servicios:
        servicio["totalServicio"] = calcular_total(servicio)

    return servicios

def filtrar_por_tipo(servicios:list, tipo_seleccionado:str, archivo_salida:str):
    """genera un archivo, pero donde solo aparezcan servicios del tipo seleccionado (1-2-3)

    Args:
        servicios (list): lista de los servicios
        tipo_seleccionado (str): 
        archivo_salida (str): 
    """
    servicios_filtrados = []
    for servicio in servicios:
        if servicio['tipo'] == tipo_seleccionado:
            servicios_filtrados.append(servicio)
    with open(archivo_salida, 'w') as archivo:
        json.dump(servicios_filtrados, archivo, indent = 4)

def ordenar(servicios:list)->list:
    """Ordena de forma ascendente

    Args:
        servicios (list): lista de los servicios

    Returns:
        list: 
    """
    for i in range(len(servicios)-1):
        for j in range(i+1, len(servicios)):
            if servicios[i]["descripcion"] > servicios[j]["descripcion"]:
                aux = servicios[i]
                servicios[i] = servicios[j]
                servicios[j] = aux

    return servicios

def mostrar_servicios_ordenados(servicios:list)->list:
    """Printea los servicios de forma ordenada

    Args:
        servicios (list): lista de los servicios

    Returns:
        list: 
    """
    servicios_ordenados = ordenar(servicios)

    imprimir_lista(servicios_ordenados)

    return servicios_ordenados

def guardar_servicios(servicios_ordenados:list , archivo_salida:str):
    """Guarda los servicios de forma ordenada en un archivo

    Args:
        servicios_ordenados (list): _description_
        archivo_salida (str): _description_
    """
    with open(archivo_salida, 'w') as archivo:
        json.dump(servicios_ordenados, archivo, indent = 4)