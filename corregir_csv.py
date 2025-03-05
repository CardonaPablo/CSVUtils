from cargar_csv import cargar_csv
from menu_utils import crear_menu_de_opciones
from corregir_registro_csv import corregir_registro_csv
import pandas as pd

def corregir_registros(incorrectos):
    registros_corregidos = []
    for indice, fila in incorrectos.iterrows():
        print(f"Registro {fila}")
        fila_corregida = corregir_registro_csv(fila, indice)
        if(fila_corregida is not None):
            print(f"Registro corregido {fila_corregida}")
            registros_corregidos.append(fila_corregida)
    
    print("Registros corregidos.", len(registros_corregidos))
    
    return pd.DataFrame(registros_corregidos)

def mostrar_menu_corregir(n_registros_incorrectos):
    return crear_menu_de_opciones(f"Se encontraron {n_registros_incorrectos} registros incorrectos.\nDesea corregir los registros afectados?", {'1': 'Si', '2': 'No'})

def corregir_csv(ruta_archivo):
    df_errores, _ = cargar_csv(ruta_archivo, validar=False)
    print()
    if len(df_errores) == 0:
        print("No hay registros incorrectos.")
        input("Presione Enter para continuar...")
        return
    
    respuesta = mostrar_menu_corregir(len(df_errores))
    if respuesta == '1':
       return corregir_registros(df_errores)

    ("Saliendo sin corregir registros.")
    return None