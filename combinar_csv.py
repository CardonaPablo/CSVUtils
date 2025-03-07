import pandas as pd
from menu_utils import crear_menu_de_opciones
import os

def combinar_csv(df_original, df_corregido, nombre_archivo):
    os.system('clear')
    print()
    respuesta = crear_menu_de_opciones(str(len(df_corregido)) + " registros corregidos.\n" + "Desea combinar los registros corregidos con el archivo original?", {'1': 'Si', '2': 'No'})
    if respuesta == '1':
        print("Combinando registros...")
        df_combinado = pd.concat([df_original, df_corregido]).drop_duplicates().reset_index(drop=True)
        combinado_nombre_archivo = "exports/" + nombre_archivo.replace('.csv', '_combinado.csv')
        df_combinado.to_csv(combinado_nombre_archivo, index=False)
        print(f"Archivo combinado guardado como {combinado_nombre_archivo}")
        return df_combinado, combinado_nombre_archivo
    else:
        print("No se combinaron los archivos.")
        return df_original, nombre_archivo
 