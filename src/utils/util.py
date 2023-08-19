import os


def check_is_dir_exists(dir):
    uri_dir = f"{dir}"
    if not os.path.exists(uri_dir):
        try:
            os.makedirs(uri_dir)
            print(f"Directorio '{dir}' creado exitosamente.")
        except OSError as error:
            print(f"No se pudo crear el directorio '{dir}': {error}")
    else:
        print(f"El directorio '{dir}' ya existe.")
