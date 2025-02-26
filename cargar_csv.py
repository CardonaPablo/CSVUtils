import pandas as pd
import re

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
