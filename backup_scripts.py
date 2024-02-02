import os
import shutil
from tkinter import messagebox


BACKUP_PATH = "./BACKUP"
EDITORES_EXTERNOS_PATH = "./Pruebas/EDITORES EXTERNOS"
FILMMAKERS_PATH = "./Pruebas/FILMMAKERS"
CONNECT_PATH = "./Pruebas/CONNECT"
LOGO_PATH = "./Stpdn_Logos_Color.png"
DATA_PATH = "./Pruebas/DATA"
PLANTILLA_PATH = "./Plantillas carpetas para copiar"


def copiar_estructura_data(tipo_proyecto, cliente, proyecto):
    ruta_cliente = os.path.join(DATA_PATH, tipo_proyecto, cliente)
    ruta_proyecto = os.path.join(ruta_cliente, proyecto)
    plantilla_proyecto = os.path.join(PLANTILLA_PATH, "Nombre de Proyecto")
    ruta_graphic = os.path.join(ruta_cliente, "0. Graphic")
    plantilla_graphic = os.path.join(PLANTILLA_PATH, "0. Graphic")

    # Crear directorio del cliente si no existe
    if not os.path.exists(ruta_cliente):
        os.makedirs(ruta_cliente)
        print(f"Directorio del cliente creado en DATA: {ruta_cliente}")

    # Verificar y copiar la carpeta "0. Graphic" si no existe
    if not os.path.exists(ruta_graphic):
        shutil.copytree(plantilla_graphic, ruta_graphic)
        print(f"Carpeta '0. Graphic' copiada en DATA: {ruta_graphic}")
        messagebox.showinfo("Éxito", f"La carpeta '0. Graphic' se ha copiado correctamente en el cliente '{cliente}'.")
    else:
        print(f"La carpeta '0. Graphic' ya existe en DATA: {ruta_graphic}")

    # Copiar la estructura de la plantilla al proyecto si el proyecto no existe
    if not os.path.exists(ruta_proyecto):
        shutil.copytree(plantilla_proyecto, ruta_proyecto)
        print(f"Estructura copiada a DATA ({tipo_proyecto}): {ruta_proyecto}")
        messagebox.showinfo("Éxito", f"La estructura del proyecto '{proyecto}' en DATA ({tipo_proyecto}) se ha copiado correctamente.")
    else:
        print(f"El proyecto ya existe en DATA ({tipo_proyecto}): {ruta_proyecto}")
        messagebox.showinfo("Información", "El proyecto ya existe en DATA y no se sobrescribirá.")

def get_folder_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)
    return total_size / (1024 * 1024)  # Convertir a MB


def move_project_to_backup_from_data(project_name):
    data_moved_successfully = False
    for project_type in ["PROYECTOS", "SEGUIMIENTOS"]:
        for client in os.listdir(os.path.join(DATA_PATH, project_type)):
            source_data = os.path.join(DATA_PATH, project_type, client, project_name)
            if os.path.exists(source_data):
                backup_data = os.path.join(BACKUP_PATH, project_type, client, project_name)
                if not os.path.exists(backup_data):
                    os.makedirs(os.path.dirname(backup_data), exist_ok=True)
                    shutil.move(source_data, backup_data)
                    print(f"Proyecto '{project_name}' movido a Backup desde DATA.")
                    data_moved_successfully = True
                else:
                    print(f"El proyecto '{project_name}' ya existe en Backup (DATA).")
                break  # Salir del bucle una vez que se encuentra el proyecto
        if data_moved_successfully:
            break  # Salir del bucle si se movió el proyecto con éxito

    if data_moved_successfully:
        messagebox.showinfo("Éxito", f"Proyecto '{project_name}' movido exitosamente a Backup desde DATA.")
        return True
    else:
        messagebox.showerror("Error", f"No se encontró el proyecto '{project_name}' en DATA para mover a Backup.")
        return False

def move_editores_externos_to_backup(project_name):
    for project_type in ["PROYECTOS", "SEGUIMIENTOS"]:
        for client in os.listdir(os.path.join(EDITORES_EXTERNOS_PATH, project_type)):
            source_folder = os.path.join(EDITORES_EXTERNOS_PATH, project_type, client, project_name, f"4. Ext. {project_name}")
            if os.path.exists(source_folder):
                backup_folder = os.path.join(BACKUP_PATH, project_type, client, project_name, f"4. Ext. {project_name}")
                if not os.path.exists(backup_folder):
                    os.makedirs(backup_folder, exist_ok=True)
                    shutil.move(source_folder, backup_folder)
                    print(f"Carpeta '4. Ext. {project_name}' movida a Backup desde EDITORES EXTERNOS.")
                    return True
                else:
                    print(f"La carpeta '4. Ext. {project_name}' ya existe en Backup.")
    print(f"No se encontró la carpeta '4. Ext. {project_name}' en EDITORES EXTERNOS.")
    return False

    # # Eliminar la carpeta de FILMMAKERS si es menor a 10MB
    # filmmakers_path = os.path.join(FILMMAKERS_PATH, tipo, project_name)
    # if os.path.exists(filmmakers_path) and get_folder_size(filmmakers_path) < 10:
    #     try:
    #         shutil.rmtree(filmmakers_path)
    #         print(f"Carpeta de FILMMAKERS eliminada: {filmmakers_path}")
    #     except Exception as e:
    #         print(f"Error al eliminar carpeta de FILMMAKERS: {e}")

    # if success:
    #     messagebox.showinfo("Éxito", "Proyecto enviado a Backup exitosamente.")
    # else:
    #     messagebox.showerror("Error", "Ocurrió un error al enviar el proyecto a Backup.")

def start_backup(project_name):
    # Obtener tipo de proyecto y cliente
    project_type, client_name = find_project_details(project_name)
    if project_type and client_name:
        # Iniciar transferencias paralelas
        if move_project_to_backup_from_data(project_name):
            if not move_editores_externos_to_backup(project_name):
                messagebox.showerror("Error", "No se pudo mover la carpeta de EDITORES EXTERNOS.")
        else:
            messagebox.showerror("Error", "No se pudo mover la carpeta de DATA.")
    else:
        messagebox.showerror("Error", "No se pudo encontrar detalles del proyecto.")