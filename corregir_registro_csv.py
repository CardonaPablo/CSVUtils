from cargar_csv import validar_csv
from tabulate import tabulate
import os
import readchar


def corregir_registro_csv(fila, indice):
 
    def mostrar_registro(fila, indice):
        os.system('clear')
        headers = fila.index.tolist()
        values = fila.values.tolist()
        table = [[f">>> {val} <<<" if i == indice else val for i, val in enumerate(values)]]
        print(tabulate(table, headers=headers, tablefmt='grid'))

    def editar_campo(fila, campo, indice):
        while True:
            valor_actual = fila[campo]
            nuevo_valor = input(f"Nuevo valor para {campo} (actual: {valor_actual}): ") or valor_actual

            # Validar que el nuevo input sea válido
            fila[campo] = nuevo_valor
            indice_error = validar_csv(fila, retornar_indices_error=True)
            if indice_error is not indice:
                return fila
            
            print("Valor inválido, ingrese otro.")
            fila[campo] = valor_actual
        


    def navegar_y_editar(fila, indice):
        campos = list(fila.index)
        while True:
            mostrar_registro(fila, indice)
            print(f"Editando campo: {campos[indice]}")
            print("Comandos: [Enter] Editar, [←/→] Navegar, [s] Guardar, [d] Descartar: ")
            comando = readchar.readkey()
            if comando == readchar.key.ENTER:  
                fila = editar_campo(fila, campos[indice], indice)
            elif comando == 's':
                return fila
            elif comando == 'd':
                return None
            elif comando == readchar.key.LEFT:
                indice = (indice - 1) % len(campos)
            elif comando == readchar.key.RIGHT:
                indice = (indice + 1) % len(campos)

    indice_error = validar_csv(fila, retornar_indices_error=True)
    indice = indice_error if indice_error is not None else 0
    fila = navegar_y_editar(fila, indice)
    return fila

