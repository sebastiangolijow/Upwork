import os
import shutil
from tkinter import messagebox


BACKUP_PATH = "./BACKUP"
LOGO_PATH = "./logo_black.png"

def get_folder_size_int(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)
    return total_size / (1024 * 1024)  # Convertir a MB

def move_folders(source_data, backup_data):
    if os.path.exists(source_data):
        try:
            if not os.path.exists(backup_data):
                os.makedirs(backup_data, exist_ok=True)
            for item in os.listdir(source_data):
                item_path = os.path.join(source_data, item)
                if os.path.isdir(item_path):
                    shutil.move(item_path, backup_data)
            shutil.rmtree(source_data)
            return True, ""
        except Exception as e:
            return False, e

def delete_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' and its contents have been deleted.")
    except Exception as e:
        print(f"An error occurred while deleting the folder '{folder_path}': {e}")

def find_client_folder(backup_root, client_name):
    seguimientos_root = os.path.join(backup_root, "SEGUIMIENTOS")
    proyectos_root = os.path.join(backup_root, "PROYECTOS")

    for root in [seguimientos_root, proyectos_root]:
        for dirpath, dirnames, filenames in os.walk(root):
            if client_name in dirnames:
                return os.path.join(dirpath)
    return None

def move_project_to_backup(project_path):
    source_data = os.path.join(project_path)
    if os.path.exists(source_data):
        folder_size = get_folder_size_int(source_data)
        if folder_size < 0:
            messagebox.showinfo(f"La carpeta {source_data} esta vacia, por lo que no la moveremos a backup.")
            return True
        if "FILMMAKERS" in source_data and folder_size < 10:
            messagebox.showinfo("Delete", "La carpeta Filmmakers esta vacia, por lo que sera eliminada.")
            delete_folder(source_data)
            return True
        project_name = source_data.split('/')[-1]
        client_name = source_data.split('/')[-2]
        if "/PROYECTOS/" in project_path:
            backup_data_path = BACKUP_PATH + "/PROYECTOS"
        if "/SEGUIMIENTOS/" in project_path:
            backup_data_path = BACKUP_PATH + "/SEGUIMIENTOS"
        if not "/SEGUIMIENTOS/" in project_path and not "/PROYECTOS/" in project_path:
            backup_data_path = find_client_folder(BACKUP_PATH, client_name)
        backup_data = (os.path.join(backup_data_path, client_name, project_name) + '/DATA') if "DATA" in source_data else ((os.path.join(backup_data_path, client_name, project_name) + '/EDITORES EXTERNOS') if "EDITORES EXTERNOS" in source_data else (os.path.join(backup_data_path, client_name, project_name) + '/FILMMAKERS'))
        if not os.path.exists(backup_data):
            os.makedirs(os.path.dirname(backup_data), exist_ok=True)
        print(backup_data)
        is_data_moved, _ = move_folders(source_data, backup_data)
        if is_data_moved:
            print(f"Proyecto '{project_name}' movido a Backup desde DATA.")
            messagebox.showinfo("Éxito", f"Proyecto '{project_name}' movido exitosamente a Backup.\nEl proyecto sera eliminado de {project_path}")
        else:
            print(f"Error al mover proyecto: {_}")
            messagebox.showinfo("Error", f"El Proyecto:'{project_name}' no se ha movido a Backup.\n Error: {_}")
    else:
        messagebox.showerror("Error", f"No se encontró el proyecto '{project_name}' en {project_path} para mover a Backup.")
