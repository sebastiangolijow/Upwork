import os
import shutil
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from tkinter import ttk


BACKUP_PATH = "./BACKUP"
EDITORES_EXTERNOS_PATH = "./EDITORES EXTERNOS"
FILMMAKERS_PATH = "./FILMMAKERS"
CONNECT_PATH = "./CONNECT"
LOGO_PATH = "./Stpdn_Logos_Color.png"
DATA_PATH = "./DATA"
PLANTILLA_PATH = "./Plantillas carpetas para copiar"

def create_folder_table(root, folder_path):
    tree = ttk.Treeview(root, columns=('Folder Name', 'Size', 'Last Modified', 'Actions'), show='headings')
    tree.heading('Folder Name', text='Folder Name')
    tree.heading('Size', text='Size')
    tree.heading('Last Modified', text='Last Modified')
    tree.heading('Actions', text='Actions')
    tree.pack(expand=True, fill=tk.BOTH)

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    for folder_name in os.listdir(folder_path):
        folder_full_path = os.path.join(folder_path, folder_name)
        if os.path.isdir(folder_full_path):
            size = get_folder_size(folder_full_path)
            last_modified = get_last_modified(folder_full_path)
            tree.insert('', 'end', values=(folder_name, size, last_modified, create_delete_button(tree, folder_full_path)))

def delete_folder(tree, folder_path):
    try:
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' and its contents have been deleted.")
        refresh_table(tree)
    except Exception as e:
        print(f"An error occurred while deleting the folder '{folder_path}': {e}")

def refresh_table(tree):
    tree.delete(*tree.get_children())  # Clear existing data
    folder_path = '/path/to/your/folder'  # Replace this with the actual folder path
    create_folder_table(tree, folder_path)


def get_last_modified(folder_path):
    last_modified_timestamp = os.path.getmtime(folder_path)
    last_modified_datetime = datetime.fromtimestamp(last_modified_timestamp)
    return last_modified_datetime.strftime('%Y-%m-%d %H:%M:%S')

def create_delete_button(tree, folder_path):
    delete_button = ttk.Button(tree, text="Delete", command=lambda: delete_folder(tree, folder_path))
    return delete_button

def get_folder_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)
    return total_size / (1024 * 1024)  # Convertir a MB

def move_folders(source_data, backup_data):
    if os.path.exists(source_data):
        for item in os.listdir(source_data):
            item_path = os.path.join(source_data, item)
            if os.path.isdir(item_path):
                shutil.move(item_path, backup_data)

def delete_folder(folder_path):
    try:
        # Delete the folder and its contents
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' and its contents have been deleted.")
    except Exception as e:
        print(f"An error occurred while deleting the folder '{folder_path}': {e}")

def move_project_to_backup_from_data(project_name, client_name):
    data_moved_successfully = False
    for project_type in ["PROYECTOS", "SEGUIMIENTOS"]:
        source_data = os.path.join(DATA_PATH, project_type, client_name, project_name)
        if os.path.exists(source_data):
            backup_data = os.path.join(BACKUP_PATH, project_type, client_name, project_name) + '/DATA'
            if not os.path.exists(backup_data):
                os.makedirs(os.path.dirname(backup_data), exist_ok=True)
                move_folders(source_data, backup_data)
                print(f"Proyecto '{project_name}' movido a Backup desde DATA.")
                data_moved_successfully = True
            else:
                print(f"El proyecto '{project_name}' ya existe en Backup (DATA).")
            break  # Salir del bucle una vez que se encuentra el proyecto

    if data_moved_successfully:
        messagebox.showinfo("Éxito", f"Proyecto '{project_name}' movido exitosamente a Backup desde DATA.")
        return True
    else:
        messagebox.showerror("Error", f"No se encontró el proyecto '{project_name}' en DATA para mover a Backup.")
        return False

def move_editores_externos_to_backup(project_name, client_name):
    for project_type in ["PROYECTOS", "SEGUIMIENTOS"]:
        # source_folder = os.path.join(EDITORES_EXTERNOS_PATH, project_type, client, project_name, f"4. Ext. {project_name}")
        source_folder = os.path.join(EDITORES_EXTERNOS_PATH, project_type, client_name, project_name)
        folder_size = get_folder_size(source_folder)
        if folder_size < 0:
            messagebox.showinfo("La carpeta Editores Externos esta vacia, por lo que no la moveremos a backup.")
            return True
        if not os.path.exists(source_folder):
            print(f"No se encontró la carpeta {project_name} en EDITORES EXTERNOS en {project_type}.")
            return True
        backup_folder = os.path.join(BACKUP_PATH, project_type, client_name, project_name)
        if not os.path.exists(backup_folder):
            print('Creating backup folder...')
            os.makedirs(backup_folder, exist_ok=True)
            editores_externos_backup_folder_source = os.path.join(BACKUP_PATH, project_type, client_name, project_name)
        editores_externos_backup_folder_source = backup_folder + '/Editores Externos'
        os.makedirs(editores_externos_backup_folder_source, exist_ok=True)
        print('Creating Editores Externos folder in backup...')
        move_folders(source_folder, editores_externos_backup_folder_source)
        messagebox.showinfo("Éxito", f"Proyecto '{project_name}' movido exitosamente a Backup desde Editores Externos.")
        print(f"{project_name}' movido a Backup desde EDITORES EXTERNOS.")
    return False

def move_or_delete_filmmakers_folder(project_name, client_name):
    for project_type in ["PROYECTOS", "SEGUIMIENTOS"]:
        source_folder = os.path.join(FILMMAKERS_PATH, project_type, client_name, project_name)
        folder_size = get_folder_size(source_folder)
        if folder_size < 10:
            messagebox.showinfo("La carpeta Filmmakers esta vacia, por lo que sera eliminada.")
            delete_folder(source_folder)
            return True
        backup_folder = os.path.join(BACKUP_PATH, project_type, client_name, project_name) + '/Filmmakers'
        print('Creating Filmmakers folder in backup...')
        move_folders(source_folder, backup_folder)
        messagebox.showinfo("Éxito", f"Proyecto '{project_name}' movido exitosamente a Backup desde Filmmakers.")
        print(f"{project_name}' movido a Backup desde Filmmakers.")

def start_backup(project_type, client_name, project_name):
    root = tk.Tk()
    root.geometry("600x400")
    create_folder_table(root, os.path.join('./FTP 24.7 v2', client_name))
    # if project_type and client_name:
    #     # Iniciar transferencias paralelas
    #     if move_project_to_backup_from_data(project_name, client_name):
    #         if not move_editores_externos_to_backup(project_name, client_name):
    #             messagebox.showerror("Error", "No se pudo mover la carpeta de EDITORES EXTERNOS.")
    #     else:
    #         messagebox.showerror("Error", "No se pudo mover la carpeta de DATA.")
    # else:
    #     messagebox.showerror("Error", "No se pudo encontrar detalles del proyecto.")