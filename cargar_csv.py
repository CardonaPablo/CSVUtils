import pandas as pd
import re
import csv 
import os
import json

verbose = False

def validar_csv(fila, retornar_indices_error=False):
    # Validar id para que sea un número
    numero_regexp = r'^[0-9]+$'
    # Validar nombre para ser un string
    string_regexp = r'^[a-zA-ZáéíóúÁÉÍÓÚñ\s]+$'
    # Validar correo para que sea un email
    correo_regexp = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    id, nombre, apellido, correo = fila

    global verbose
    if pd.isna(id) or not re.match(numero_regexp, str(id)):
        if verbose:
            print(id, 'El id no es un número')
        if retornar_indices_error:
            return 0
        return False
    if pd.isna(nombre) or not re.match(string_regexp, nombre):
        if verbose:
            print(id, 'El nombre no es un string')
        if retornar_indices_error:
            return 1
        return False
    if pd.isna(apellido) or not re.match(string_regexp, apellido):
        if verbose:
            print(id, 'El apellido no es un string')
        if retornar_indices_error:
            return 2
        return False
    if pd.isna(correo) or not re.match(correo_regexp, correo):
        if verbose:
            print(id, 'El correo no es un correo')
        if retornar_indices_error:
            return 3
        return False
    
    return True

def cargar_csv(nombre_archivo, validar=True):
    df = pd.read_csv(nombre_archivo)
    df_errores = pd.DataFrame(columns=df.columns)

    for indice, fila in df.iterrows():
        if validar:
            valido = validar_csv(fila)
            if not valido:
                df_errores = pd.concat([df_errores, pd.DataFrame([fila])], ignore_index=True)
                df.drop(indice, inplace=True)

    df.reset_index(drop=True, inplace=True)
    df = df.drop_duplicates()
    df_errores = df_errores.drop_duplicates()


    return [df, df_errores]

def procesar_csv(archivo_entrada):

    from corregir_csv import corregir_csv
    from combinar_csv import combinar_csv

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

    errores_nombre_archivo = "exports/" + nombre_archivo.replace('.csv', '_errores.csv')
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

