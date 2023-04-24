import os

# Directorio de origen
src_dir = "./"
# Fichero de destino
dst_file = "destino.gift"

# Abrir fichero de destino en modo escritura
with open(dst_file, "w") as dst:
    # Recorrer todos los ficheros en el directorio de origen
    for filename in os.listdir(src_dir):
        # Comprobar que el fichero es de texto
        if filename.endswith(".md") and filename != dst_file:
            # Abrir fichero de origen en modo lectura
            with open(os.path.join(src_dir, filename), "r") as src:
                # Leer contenido del fichero de origen
                src_content = src.read()
                # Escribir contenido del fichero de origen en el fichero de destino
                dst.write(src_content)

