import os
import shutil
from tkinter import messagebox


BACKUP_PATH = "./BACKUP"
EDITORES_EXTERNOS_PATH = "./EDITORES EXTERNOS"
FILMMAKERS_PATH = "./FILMMAKERS"
CONNECT_PATH = "./CONNECT"
LOGO_PATH = "./Stpdn_Logos_Color.png"
DATA_PATH = "./DATA"
PLANTILLA_PATH = "./Plantillas carpetas para copiar"

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

def start_backup(project_type, client_name, project_name):
    # Obtener tipo de proyecto y cliente
    if project_type and client_name:
        # Iniciar transferencias paralelas
        if move_project_to_backup_from_data(project_name):
            if not move_editores_externos_to_backup(project_name):
                messagebox.showerror("Error", "No se pudo mover la carpeta de EDITORES EXTERNOS.")
        else:
            messagebox.showerror("Error", "No se pudo mover la carpeta de DATA.")
    else:
        messagebox.showerror("Error", "No se pudo encontrar detalles del proyecto.")