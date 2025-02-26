import os

def obtener_respuesta_valida(prompt, opciones):
    while True:
        print(prompt)
        for clave, etiqueta in opciones.items():
            print(f"{clave}: {etiqueta}")
        respuesta = input("Seleccione una opción: ")
        if respuesta in opciones.keys():
            return respuesta
        os.system('clear')
        print("Opción no válida. Intente de nuevo.")

