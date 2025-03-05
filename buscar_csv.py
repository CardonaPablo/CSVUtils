import os
import pandas as pd

from menu_utils import crear_menu_de_opciones

field_to_idx = { 'id': 0, 'first_name': 1, 'last_name': 2, 'email': 3 }
idx_to_field = { '1': 'id', '2': 'first_name', '3': 'last_name', '4': 'email' }
verbose = False

def mostrar_interfaz_elegir_campo():
    global idx_to_field
    while True:
        opcion = crear_menu_de_opciones("Elegir campo", idx_to_field)
        os.system('clear')
        print("Campo seleccionado", idx_to_field[opcion])
        return idx_to_field[opcion]

def buscar_por_campo(campo, valor, user_data):
    global verbose
    if(verbose):
        print("*********************")
        print("Buscando por campo", campo, "con query", valor)
    
    # Filtrar el DataFrame por el campo y query
    users_found = user_data[user_data[campo].str.contains(valor, case=False, na=False)]
    
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

def mostrar_menu_busqueda(user_data):

    os.system('clear')
    print("Bienvenido al buscador de usuarios")
    queries = []
    resultados = user_data

    while True:
        os.system('clear')
        if len(queries) > 0:
            print("Filtros aplicados:")
            for query in queries:
                print(f"{query['campo']} = {query['valor']}")  
        campo = mostrar_interfaz_elegir_campo()
        valor = input("Ingrese el valor a buscar: ")

        resultados = buscar_por_campo(campo, valor, resultados)
        if not resultados.empty:
            print("Resultados encontrados:")
            print(resultados)
            input("Presione enter para continuar...")
        else:
            print("No se encontraron usuarios")
            input("Presione enter para volver...")
            break
        opcion_multiples_filtros = crear_menu_de_opciones("Desea aplicar más filtros?", {'1': 'Sí', '2': 'No'})
        if opcion_multiples_filtros == '1':
            queries.append({'campo': campo, 'valor': valor})
        if opcion_multiples_filtros == '2':
            break
        



