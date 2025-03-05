import os
import readchar

def crear_menu_de_opciones(prompt, opciones):
    
    BOX_HORIZONTAL = "─"
    BOX_VERTICAL = "│"
    BOX_TOP_LEFT = "┌"
    BOX_TOP_RIGHT = "┐"
    BOX_BOTTOM_LEFT = "└"
    BOX_BOTTOM_RIGHT = "┘"
    BOX_TEE_RIGHT = "├"
    BOX_TEE_LEFT = "┤"
    
    opciones_list = list(opciones.items())
    option_texts = [f"{clave}: {etiqueta}" for clave, etiqueta in opciones_list]
    max_content_len = max([len(text) for text in option_texts])
    
    # Obtener la logngitud del prompt para determinar el ancho del box
    prompt_lines = prompt.split('\n')
    if prompt_lines:
        max_content_len = max(max_content_len, max([len(line) for line in prompt_lines]))
    
    box_width = max_content_len + 4  # 1 por cada barra vertical + 1 por cada espacio de padding
    selected = 0
    
    while True:
        
        os.system('clear')
        # Borde arriba, (-2 para tomar en cuanta las esquinas)
        print(f"{BOX_TOP_LEFT}{BOX_HORIZONTAL * (box_width - 2)}{BOX_TOP_RIGHT}")
        
        # prompt
        for line in prompt_lines:
            padding = " " * (max_content_len - len(line))
            print(f"{BOX_VERTICAL} {line}{padding} {BOX_VERTICAL}")
        
        # separador
        print(f"{BOX_TEE_RIGHT}{BOX_HORIZONTAL * (box_width - 2)}{BOX_TEE_LEFT}")
        
        # opciones
        for i, (clave, etiqueta) in enumerate(opciones_list):
            option_text = f"{clave}: {etiqueta}"
            padding = " " * (max_content_len - len(option_text))
            
            if i == selected:
                print(f"{BOX_VERTICAL} \033[7m{option_text}\033[0m{padding} {BOX_VERTICAL}")
            else:
                print(f"{BOX_VERTICAL} {option_text}{padding} {BOX_VERTICAL}")
        
        # Borde abajo
        print(f"{BOX_BOTTOM_LEFT}{BOX_HORIZONTAL * (box_width - 2)}{BOX_BOTTOM_RIGHT}")
        
        key = readchar.readkey()
        if key == readchar.key.UP and selected > 0:
            selected -= 1
        elif key == readchar.key.DOWN and selected < len(opciones_list) - 1:
            selected += 1
        elif key == readchar.key.ENTER:
            return opciones_list[selected][0]
        elif key == readchar.key.ESC:
            return None

