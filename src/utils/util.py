import os
from configs.config_const import TOTAL_PAGES_TO_PROCESS, STEP_PAGES


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

def get_total_pages(last_page: int) -> list:
    return range(last_page + 1, TOTAL_PAGES_TO_PROCESS, STEP_PAGES)
