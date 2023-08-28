import re
import tkinter as tk
from tkinter import filedialog


# Lee la lista de tokens desde un archivo
def leer_lista_tokens(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        lines = archivo.readlines()
    tokens = []
    for line in lines:
        parts = line.strip().split(',')
        if len(parts) == 3:
            tokens.append({"nombre": parts[0], "regex": parts[1], "codigo": parts[2]})
    return tokens

# Lee el código fuente desde un archivo
def leer_codigo_fuente(ruta_archivo, lista_tokens):
    with open(ruta_archivo, 'r') as archivo:
        codigo_fuente = archivo.read()
    codigo_fuente = eliminar_comentarios(codigo_fuente, lista_tokens)
    return codigo_fuente

# Elimina los comentarios y su contenido del código fuente
def eliminar_comentarios(codigo_fuente, lista_tokens):
    # Utiliza una expresión regular para encontrar y reemplazar los comentarios
    codigo_fuente = re.sub(lista_tokens[0]["regex"], '', codigo_fuente, flags=re.DOTALL)
    print("-----------------------------------codigo sin comentarios ------------------------------------------ ", codigo_fuente)
    return codigo_fuente

# Tokeniza el código fuente
def tokenizar_codigo_fuente(codigo_fuente, tokens):
    lexemas = []
    posicion = 0

    while posicion < len(codigo_fuente):
        coincidencia = None

        for token in tokens:
            regex = token["regex"]
            patron = re.compile(regex)
            coincidencia = patron.match(codigo_fuente, posicion)
            
            if coincidencia:
                lexema = coincidencia.group(0)
                if token["nombre"] != "Comentario":
                    lexemas.append([token["codigo"], lexema, coincidencia.start(), coincidencia.end()])
                posicion = coincidencia.end()
                break
        
        if not coincidencia:
            posicion += 1
    
    return lexemas

def mostrar_resultado(lexemas):
    root = tk.Tk()
    root.title("Lexemas")

    textlexemas = ""
    for lexema in lexemas:
        textlexemas += lexema[0] + " -> " + lexema[1] + "->" + str(lexema[2]) + "," + str(lexema[3]) +   "\n"
    

    
    lexemas_label = tk.Label(root,text=textlexemas)
    lexemas_label.config(width=100)
    lexemas_label.pack()
    root.mainloop()



# Función principal
def principal():
    lista_tokens = leer_lista_tokens('tokens.txt')
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    print(file_path)


    codigo_fuente = leer_codigo_fuente(file_path, lista_tokens)
    lexemas = tokenizar_codigo_fuente(codigo_fuente, lista_tokens)
    print("-----------------------------------lexemas ------------------------------------------ ")
    for lexema in lexemas:
        print(lexema[2])

    mostrar_resultado(lexemas)


if __name__ == "__main__":
    principal()
