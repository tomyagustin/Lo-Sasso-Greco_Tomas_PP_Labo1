from funciones import *
def main():
    bandera = False
    while True:
        menu()
        opcion = input("Seleccion una opción: ")
        match(opcion):
            case '1':
                bandera = True
                archivo = cargar_archivo("parcial/data.json")
                print("\nArchivo creado exitosamente. ")
            case '2':
                imprimir_lista(archivo)
            case '3':
                if bandera == True:
                    servicios_actualizados = asignar_totales(archivo)
                    print("\nTotal servicio asignado. ")
                    #for servicio in servicios_actualizados:
                        #print(servicio)
            case '4':
                if bandera == True:
                    filtrar_por_tipo(archivo, "2", "parcial/servicios_filtrados.json")
                    print("\nArchivo creado exitosamente. ")
            case '5':
                if bandera == True:
                    servicios_ordenados = mostrar_servicios_ordenados(archivo)
                    print("\nLos servicios fueron ordenados. ")
            case '6':
                if bandera == True:
                    guardar_servicios(servicios_ordenados, "parcial/servicios_ordenados.json")
                    print("\nArchivo creado exitosamente. ")
            case '7':
                print("Programa finalizado.\n")
                break
            case _:
                print("La opcion no existe")

main()