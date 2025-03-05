import os
from cargar_csv import procesar_csv
from buscar_csv import mostrar_menu_busqueda
from exportar_archivo import exportar_archivo
from menu_utils import crear_menu_de_opciones
verbose = False

def cargar_archivo_inicial():
    global verbose
    user_data = procesar_csv('user_data.csv')
    if(verbose):
        print("CSV cargado con éxito")
        print(len(user_data), 'registros cargados')
    return user_data

def mostrar_menu_principal(user_data):
    os.system('clear')
    print("*********************")
    return crear_menu_de_opciones(f"Registros cargados: {len(user_data)}", {
        '1': 'Buscar por múltiples campos',
        '2': 'Exportar archivo',
        '3': 'Salir'
    })

if __name__  == "__main__": 
    user_data = cargar_archivo_inicial()
    while True:
        opcion_seleccionada = mostrar_menu_principal(user_data)
        if(opcion_seleccionada == '1'):
            mostrar_menu_busqueda(user_data)
        elif(opcion_seleccionada == '2'):
            exportar_archivo('user_data')
        elif(opcion_seleccionada == '3'):
            break
