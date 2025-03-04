import csv 
from cargar_csv import cargar_csv
from corregir_csv import corregir_csv
from combinar_csv import combinar_csv
import os
import json
import pandas as pd

field_to_idx = { 'id': 0, 'first_name': 1, 'last_name': 2, 'email': 3 }
idx_to_field = { '1': 'id', '2': 'first_name', '3': 'last_name', '4': 'email' }
verbose = False

def procesar_csv(archivo_entrada):
    os.system('clear')
    df, df_errores = cargar_csv(archivo_entrada)
    if len(df_errores) == 0:
        crear_archivos_origen(df, archivo_entrada)
        return df

    errores_filename = crear_archivo_de_errores(df_errores, archivo_entrada)

    df_corregido = corregir_csv(errores_filename)
    if df_corregido is None:
        crear_archivos_origen(df, archivo_entrada)
        return df

    # Ajustar para guardar sólo el DataFrame y desechar el nombre de archivo
    df_combinado, _ = combinar_csv(df, df_corregido, archivo_entrada)
    crear_archivos_origen(df_combinado, archivo_entrada)

    return df_combinado

def crear_archivos_origen(df, nombre_archivo):
    crear_archivo_xml(df, nombre_archivo)
    crear_archivo_json(df, nombre_archivo)
    crear_copia_csv(df, nombre_archivo)

def crear_archivo_de_errores(df_errores, nombre_archivo):
    # Open CSV file in write mode

    errores_nombre_archivo = nombre_archivo.replace('.csv', '_errores.csv')
    with open(errores_nombre_archivo, 'w', newline='') as archivo:
        escritor = csv.writer(archivo)
    # Write header
        escritor.writerow(df_errores.columns)
    # Write error data
        for indice, fila in df_errores.iterrows():
            escritor.writerow(fila)
    return errores_nombre_archivo

def crear_archivo_xml(df, nombre_archivo):
    # Crear un archivo XML con los datos del dataframe
    # Nombre sin json
    xml_nombre_archivo = 'sources/' + nombre_archivo.replace('.csv', '.xml')
    df.to_xml(xml_nombre_archivo, root_name='usuarios', row_name='usuario')

def crear_archivo_json(df, nombre_archivo):
    # Crear 2 jsons, uno con los encabezados del csv y otro con los datos
    file_columns = df.columns.tolist()
    json_nombre_archivo = 'sources/' + nombre_archivo.replace('.csv', '_estructura.json')
    with open(json_nombre_archivo, 'w') as file:
        json.dump(file_columns, file, indent=4)

    df.to_json('sources/' + nombre_archivo.replace('.csv', '_datos.json'), orient='records', indent=4)

def crear_copia_csv(df, nombre_archivo):
    # Crear una copia del archivo CSV original
    copia_nombre_archivo = 'sources/' + nombre_archivo
    df.to_csv(copia_nombre_archivo, index=False)


def load_csv():
    global verbose
    user_data = procesar_csv('user_data.csv')
    if(verbose):
        print("CSV cargado con éxito")
        print(len(user_data), 'registros cargados')
    return user_data

def mostrar_interfaz_elegir_campo():
    global idx_to_field
    while True:
        print("Elegir campo")
        print("1. id")
        print("2. nombre")
        print("3. apellido")
        print("4. email")
        opcion = input("Ingrese una opción: ")
        if opcion not in ['1', '2', '3', '4']:
            print("Opción inválida")
            continue
        print("Campo seleccionado", idx_to_field[opcion])
        os.system('clear')
        return idx_to_field[opcion]

def buscar_por_campo(campo, query, user_data):
    global verbose
    if(verbose):
        print("*********************")
        print("Buscando por campo", campo, "con query", query)
    
    # Filtrar el DataFrame por el campo y query
    users_found = user_data[user_data[campo].str.contains(query, case=False, na=False)]
    
    if(verbose):
        print("Usuarios encontrados:")
        print(users_found)
    
    return users_found

def buscar_por_multiples(user_data, queries):
    global verbose
    usuarios = user_data
    for query in queries:
        if verbose:
            print("Query", str(query))
        
        # Check the data type of the column
        if usuarios[query['campo']].dtype == 'object':
            # Ensure the column is of string type
            usuarios.loc[:, query['campo']] = usuarios[query['campo']].astype(str)
            usuarios = usuarios[usuarios[query['campo']].str.contains(query['valor'], case=False, na=False)]
        else:
            # Assuming numeric comparison for non-string types
            try:
                valor = float(query['valor'])
                usuarios = usuarios[usuarios[query['campo']] == valor]
            except ValueError:
                print(f"Invalid query value for numeric field: {query['valor']}")
                return pd.DataFrame()  # Return empty DataFrame if the value is invalid
    return usuarios


if __name__  == "__main__": 
    user_data = load_csv()
    while True:
        os.system('clear')
        print("Registros cargados: ", len(user_data))
        print("*********************")
        print("Bienvenido al buscador de usuarios")

        primer_campo = mostrar_interfaz_elegir_campo()
        primer_valor = input("Ingrese la query para primer campo: ")

        segundo_campo = mostrar_interfaz_elegir_campo()
        segundo_valor = input("Ingrese la query para segundo campo: ")

        queries = []
        queries.append({
            'campo': primer_campo, 
            'valor': primer_valor
        })
        queries.append({
            'campo': segundo_campo, 
            'valor': segundo_valor
        })

        resultados = buscar_por_multiples(user_data, queries)
        if not resultados.empty:
            print("Resultados encontrados:")
            print(resultados)
        else:
            print("No se encontraron usuarios")
        print()
        print("Pulse 5 para salir")
        print("Pulse cualquier otra tecla para continuar")
        final_seleccion = input()
        if(final_seleccion == '5'):
            break


