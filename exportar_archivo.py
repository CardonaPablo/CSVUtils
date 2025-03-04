import os
import pandas as pd
import json
from menu_utils import obtener_respuesta_valida

def cargar_archivo(formato, filename):
    # Definir rutas de archivos según el formato de origen
    rutas = { 
        'CSV':  f'sources/{filename}.csv',
        'JSON': [f'sources/{filename}_datos.json', f'sources/{filename}_estructura.json'],
        'XML':  f'sources/{filename}.xml'
    }
    try:
        if formato == 'CSV':
            return pd.read_csv(rutas['CSV'])
        elif formato == 'JSON':
            df = pd.read_json(rutas['JSON'][0])
            df.columns = pd.read_json(rutas['JSON'][1])
            return df
        elif formato == 'XML':
            return pd.read_xml(rutas['XML'])
        else:
            raise ValueError(f"Formato no soportado: {formato}")
    except Exception as e:
        print(f"Error al cargar el archivo {formato}: {e}")
        return None

def exportar_a_csv(df, ruta_salida):
    """Exporta un DataFrame a formato CSV."""
    try:
        ruta_salida = f'exports/{ruta_salida}_exported.csv'
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
        df.to_csv(ruta_salida, index=False)
        print(f"Archivo exportado exitosamente como: {ruta_salida}")
        return True
    except Exception as e:
        print(f"Error al exportar a CSV: {e}")
        return False

def exportar_a_json(df, ruta_salida):
    """Exporta un DataFrame a formato JSON."""
    try:
        ruta_salida = f'exports/{ruta_salida}_exported.json'
        df.to_json(ruta_salida, orient='records')

        file_columns = df.columns.tolist()
        json_nombre_archivo = ruta_salida.replace('.json', '_estructura.json')
        with open(json_nombre_archivo, 'w') as file:
            json.dump(file_columns, file, indent=4)

        print(f"Archivo exportado exitosamente como: {ruta_salida}")
        return True
    except Exception as e:
        print(f"Error al exportar a JSON: {e}")
        return False

def exportar_a_xml(df, ruta_salida):
    """Exporta un DataFrame a formato XML."""
    try:
        ruta_salida = f'exports/{ruta_salida}_exported.xml'
        df.to_xml(ruta_salida, root_name='data', row_name='record')
        print(f"Archivo exportado exitosamente como: {ruta_salida}")
        return True
    except Exception as e:
        print(f"Error al exportar a XML: {e}")
        return False

def menu_formato_origen():
    """Muestra el menú para seleccionar el formato de origen."""
    opciones = {'1': 'CSV', '2': 'JSON', '3': 'XML'}
    respuesta = obtener_respuesta_valida("Seleccione el formato de origen:", opciones)
    return opciones[respuesta]

def menu_formato_destino(formato_origen):
    """Muestra el menú para seleccionar el formato de destino, excluyendo el formato de origen."""
    formatos = {'CSV': '1', 'JSON': '2', 'XML': '3'}
    # Eliminar el formato de origen de las opciones
    del formatos[formato_origen]
    
    opciones = {valor: clave for clave, valor in formatos.items()}
    respuesta = obtener_respuesta_valida("Seleccione el formato de destino:", opciones)
    return opciones[respuesta]

def exportar_archivo(filename):
    """Función principal que maneja el flujo de exportación de archivos."""
    os.system('clear')
    print("=== Exportación de Archivos ===")
    
    # Seleccionar formato de origen
    formato_origen = menu_formato_origen()
    formato_destino = menu_formato_destino(formato_origen)

    
    # Cargar el archivo de origen
    df = cargar_archivo(formato_origen, filename)
    
    if df is not None:
        # Definir la ruta de salida
        if formato_destino == 'CSV':
            exportar_a_csv(df, filename)
        elif formato_destino == 'JSON':
            exportar_a_json(df, filename)
        elif formato_destino == 'XML':
            exportar_a_xml(df, filename)
        
    input("Presione Enter para continuar...")


if __name__ == '__main__':
    exportar_archivo('user_data')