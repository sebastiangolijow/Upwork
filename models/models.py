import logging
import os
import shutil
import time
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from tkinter import ttk

from backup_scripts import get_folder_size, move_or_delete_filmmakers_folder
from backup_scripts import move_editores_externos_to_backup
from backup_scripts import move_project_to_backup_from_data


# from backup_scripts import start_backup


# Rutas de las carpetas destino
BACKUP_PATH = "/Users/arnau/Stupendastic Dropbox/Admin Stupendastic/Dropbox-Stupendastic/0. Scripts/Manual/Crear_nuevo_proyecto/Pruebas/Enviar a Backup"
BACKUP_PATH_TEST = "./BACKUP"
DATA_PATH = "/Users/arnau/Stupendastic Dropbox/Admin Stupendastic/Dropbox-Stupendastic/0. Scripts/Manual/Crear_nuevo_proyecto/Pruebas/DATA"
DATA_PATH_TEST = "./DATA"
EDITORES_EXTERNOS_PATH = "/Users/arnau/Stupendastic Dropbox/Admin Stupendastic/Dropbox-Stupendastic/0. Scripts/Manual/Crear_nuevo_proyecto/Pruebas/EDITORES EXTERNOS"
EDITORES_EXTERNOS_PATH_TEST = "./EDITORES EXTERNOS"
FILMMAKERS_PATH = "/Users/arnau/Stupendastic Dropbox/Admin Stupendastic/Dropbox-Stupendastic/0. Scripts/Manual/Crear_nuevo_proyecto/Pruebas/FILMMAKERS"
FILMMAKERS_PATH_TEST = "./FILMMAKERS"
CONNECT_PATH = "/Users/arnau/Stupendastic Dropbox/Admin Stupendastic/Dropbox-Stupendastic/0. Scripts/Manual/Crear_nuevo_proyecto/Pruebas/CONNECT"
CONNECT_PATH_TEST = "./CONNECT"
PLANTILLA_PATH = "/Users/arnau/Stupendastic Dropbox/Admin Stupendastic/Dropbox-Stupendastic/0. Scripts/Manual/Crear_nuevo_proyecto/Plantillas carpetas para copiar"
PLANTILLA_PATH_TEST = "./Plantillas carpetas para copiar"
LOGO_PATH = "/Users/arnau/Stupendastic Dropbox/Admin Stupendastic/Dropbox-Stupendastic/0. Scripts/Manual/Crear_nuevo_proyecto/Stpdn_Logos_Color en tamaño pequeño.png"
LOGO_PATH_TEST = "./Stpdn_Logos_Color.png"

logo = None
show_table = False
root = tk.Tk()
background_color = "#1063FF"
class TableClass:
    def __init__(self, table_root):
        self.root = table_root
        self.table_displayed = False
        self.is_packed = False  # Track packing state
        self.tree = False
        self.path= ""
        self.item_id = None
        self.delete_button = None
        self.scrollbar = None
        self.xscrollbar = None

    def create_data_table(self, data, width):
        # Create a Treeview widget
        show_table = True
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", font=("Helvetica", 12))
        delete_button = ttk.Button(self.root, text="Delete", command=lambda: self.delete_project(self.path, self.item_id))
        self.delete_button = delete_button
        tree = ttk.Treeview(self.root, columns=list(data[0].keys()), show="headings")
        self.tree = tree
        # Add columns to the Treeview
        for column in data[0].keys():
            self.tree.heading(column, text=column)
            self.tree.column(column, anchor=tk.CENTER, width=width)

        # Add data to the Treeview
        for item in data:
            values = [item[column] for column in data[0].keys()]
            self.tree.insert("", tk.END, values=(values), tags=(item["Project path"],))
        self.tree.bind("<<TreeviewSelect>>", lambda event: self.item_select(event))

        # Add a vertical scrollbar
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.scrollbar = scrollbar
        xscrollbar = ttk.Scrollbar(self.root, orient="horizontal", command=self.tree.xview)
        self.xscrollbar = xscrollbar
        self.tree.configure(xscrollcommand=xscrollbar.set, yscrollcommand=scrollbar.set)

        # Pack the Treeview and scrollbar
        if show_table:
            xscrollbar.pack(side="bottom", fill="x")
            self.tree.pack(expand=True, fill=tk.BOTH, side="left", anchor='w')

            scrollbar.pack(side="left", fill=tk.Y, padx=(0, 10))
            self.table_displayed = True
        else:
            self.tree.pack_forget()
            self.table_displayed = False

    def item_select(self, event):
        self.item_id = self.tree.selection()[0]
        project_path = self.tree.item(self.item_id)['values'][-1]
        self.path = project_path
        self.delete_button.pack(padx=5, pady=5)

    def destroy_table(self):
        self.tree.pack_forget()

    def delete_project(self, project_path, item_id):
        # Implement the logic to delete the project using the project_path
        print(f"Deleting project at path: {project_path}")
        self.tree.delete(item_id)
        shutil.rmtree(project_path)

def get_existing_clients():
    def list_dirs(path):
        return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

    project_clients = set(list_dirs(os.path.join(DATA_PATH, "PROYECTOS")))
    seguimiento_clients = set(list_dirs(os.path.join(DATA_PATH, "SEGUIMIENTOS")))
    all_clients = project_clients.union(seguimiento_clients)
    return sorted(list(all_clients))

def get_all_orders(base_path):
    all_orders = []

    # Obtener todas las carpetas en la ruta base (proyectos o seguimiento)
    for client in os.listdir(base_path):
        client_path = os.path.join(base_path, client)

        # Verificar si es un directorio
        if os.path.isdir(client_path):
            # Obtener todas las carpetas dentro del cliente (pedidos)
            orders = [order for order in os.listdir(client_path) if os.path.isdir(os.path.join(client_path, order))]
            all_orders.extend(orders)

    return sorted(all_orders)

### We could add some validation to see if the name of the project or client is available
def validate_input(client_name, project_name):
    # Validación de entradas del usuario
    if not client_name.strip():
        messagebox.showwarning("Advertencia", "El nombre del cliente no puede estar vacío.")
        return False
    if not project_name.strip():
        messagebox.showwarning("Advertencia", "El nombre del proyecto no puede estar vacío.")
        return False
    print(f"Validación exitosa: cliente '{client_name}', proyecto '{project_name}'")
    return True


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

def copiar_estructura_editores_externos(tipo_proyecto, cliente, proyecto):
    ruta_cliente = os.path.join(EDITORES_EXTERNOS_PATH, tipo_proyecto, cliente)
    plantilla = os.path.join(PLANTILLA_PATH, "EDITORES EXTERNOS", tipo_proyecto, "4. Ext. Nombre Proyecto")
    ruta_proyecto = os.path.join(ruta_cliente, proyecto, f"4. Ext. {proyecto}")  # Añadido un nivel adicional

    if not os.path.exists(ruta_cliente):
        os.makedirs(ruta_cliente)
        print(f"Directorio del cliente creado en EDITORES EXTERNOS: {ruta_cliente}")

    if not os.path.exists(ruta_proyecto):
        shutil.copytree(plantilla, ruta_proyecto)
        print(f"Estructura copiada y renombrada en EDITORES EXTERNOS ({tipo_proyecto}): {ruta_proyecto}")
        messagebox.showinfo("Éxito", f"La estructura del proyecto '{proyecto}' en EDITORES EXTERNOS ({tipo_proyecto}) se ha copiado y renombrado correctamente.")
    else:
        print(f"El proyecto ya existe en EDITORES EXTERNOS ({tipo_proyecto}): {ruta_proyecto}")
        messagebox.showinfo("Información", "El proyecto ya existe en EDITORES EXTERNOS y no se sobrescribirá.")

def copiar_estructura_filmmakers(tipo_proyecto, cliente, proyecto):
    ruta_cliente = os.path.join(FILMMAKERS_PATH, tipo_proyecto, cliente)
    plantilla = os.path.join(PLANTILLA_PATH, "FILMMAKERS", "Nombre de Proyecto")
    ruta_proyecto = os.path.join(ruta_cliente, proyecto)

    if not os.path.exists(ruta_cliente):
        os.makedirs(ruta_cliente)
        print(f"Directorio del cliente creado en FILMMAKERS: {ruta_cliente}")

    if not os.path.exists(ruta_proyecto):
        shutil.copytree(plantilla, ruta_proyecto)
        print(f"Estructura copiada en FILMMAKERS ({tipo_proyecto}): {ruta_proyecto}")
        messagebox.showinfo("Éxito", f"La estructura del proyecto '{proyecto}' en FILMMAKERS ({tipo_proyecto}) se ha copiado correctamente.")
    else:
        print(f"El proyecto ya existe en FILMMAKERS ({tipo_proyecto}): {ruta_proyecto}")
        messagebox.showinfo("Información", "El proyecto ya existe en FILMMAKERS y no se sobrescribirá.")

def copiar_estructura_connect(cliente, proyecto):
    ruta_cliente = os.path.join(CONNECT_PATH, cliente)
    plantilla_proyecto = os.path.join(PLANTILLA_PATH, "CONNECT", "Nombre de Proyecto")
    ruta_proyecto = os.path.join(ruta_cliente, proyecto)

    # Crear directorio del cliente si no existe
    if not os.path.exists(ruta_cliente):
        os.makedirs(ruta_cliente)
        print(f"Directorio del cliente creado en CONNECT: {ruta_cliente}")

    # Copiar la estructura de la plantilla al proyecto si el proyecto no existe
    if not os.path.exists(ruta_proyecto):
        shutil.copytree(plantilla_proyecto, ruta_proyecto)
        print(f"Estructura copiada en CONNECT: {ruta_proyecto}")
        messagebox.showinfo("Éxito", f"La estructura del proyecto '{proyecto}' en CONNECT se ha copiado correctamente.")
    else:
        print(f"El proyecto ya existe en CONNECT: {ruta_proyecto}")
        messagebox.showinfo("Información", "El proyecto ya existe en CONNECT y no se sobrescribirá.")

def log_activity(message):
    # Registro de actividades
    logging.basicConfig(filename="project_creator_log.txt", level=logging.INFO)
    logging.info(message)

def on_submit(combo_clients, entry_project, project_type_var):
    client_name = combo_clients.get()
    project_name = entry_project.get()
    project_type = project_type_var.get()

    if not validate_input(client_name, project_name):
        return

    copiar_estructura_data(project_type, client_name, project_name)
    copiar_estructura_editores_externos(project_type, client_name, project_name)
    copiar_estructura_filmmakers(project_type, client_name, project_name)
    copiar_estructura_connect(client_name, project_name)

    log_activity(f"Proyecto creado: {client_name} - {project_name} - {project_type}")




#PARTE BACKUP______________________________
def get_all_project_paths_in_data():
    project_paths = []
    for tipo in ["PROYECTOS", "SEGUIMIENTOS"]:
        project_path = os.path.join(DATA_PATH, tipo)
        for client in os.listdir(project_path):
            client_path = os.path.join(project_path, client)
            if os.path.isdir(client_path):
                projects = os.listdir(client_path)
                project_paths.extend(os.path.join(client_path, project) for project in projects)
    return sorted(set(project_paths))


def delete_folder(path):
    try:
        shutil.rmtree(path)
        print(f"Folder '{path}' successfully deleted.")
    except Exception as e:
        print(f"Error deleting folder '{path}': {e}")

def get_all_projects():
    projects = []
    for tipo in ["PROYECTOS", "SEGUIMIENTOS"]:
        project_path = os.path.join(DATA_PATH, tipo)
        for client in os.listdir(project_path):
            client_path = os.path.join(project_path, client)
            if os.path.isdir(client_path):
                projects.extend(os.listdir(client_path))
    return sorted(set(projects))


def folder_info_recursive(path, project_name, width, is_ftp=False):
    folders_info = []
    def check_folder(folder_path):
        files = []
        for entry in os.listdir(folder_path):
            entry_path = os.path.join(folder_path, entry)
            if os.path.isfile(entry_path):
                files.append(entry_path.lower())

        is_empty = len(files) == 0
        file_count = len([file for file in files if file.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.mp4', '.avi', '.mkv', '.mp3'))])

        # Get the last modified date of the folder
        try:
            last_modified_date = datetime.fromtimestamp(os.path.getmtime(folder_path))
        except OSError:
            last_modified_date = None
        if not is_ftp:
            return {
                'Folder name': os.path.relpath(folder_path, path),
                'Folder size': get_folder_size(folder_path),
                'Is empty': is_empty,
                'File count': file_count,
                'Last modified date': last_modified_date,
                'Editores externos size': get_folder_size(folder_path.replace('DATA', 'EDITORES EXTERNOS')),
                'Project path': folder_path,
            }
        return {
            'Folder name': os.path.relpath(folder_path, path),
            'Folder size': get_folder_size(folder_path),
            'File count': file_count,
            'Last modified date': last_modified_date,
            'Project path': folder_path,
        }

    def traverse_folder(current_path):
        for entry in os.listdir(current_path):
            entry_path = os.path.join(current_path, entry)
            if os.path.isdir(entry_path):
                folders_info.append(check_folder(entry_path))
                traverse_folder(entry_path)

    traverse_folder(path)
    global my_instance
    global delete_proyect_button
    if is_ftp:
        # new_root = tk.Tk()
        window = tk.Toplevel(root)
        window.title("FTP 24.7 folder data")
        tfp_table = TableClass(window)
        tfp_table.create_data_table(folders_info, width)
        root.wait_window(window)
        return folders_info

    has_files = any(folder['File count'] > 0 for folder in folders_info)
    if not has_files and not is_ftp:
        result_label.config(text= f"All folders inside {project_name} are empty, do you want to delete it ?", background='red')
        delete_proyect_button = tk.Button(root, text="Delete", command=lambda: delete_folder(path))
        delete_proyect_button.pack()
        return False
    else:
        try:
            delete_proyect_button.pack_forget()
        except Exception as e:
            print(e)
        my_instance = TableClass(root)
        my_instance.create_data_table(folders_info, width)
    return folders_info

def search_project(project_name):
    global send_backup_button
    folder_data = False
    project_path_f = []
    try:
        my_instance.destroy_table()
        send_backup_button.pack_forget()
        result_label.pack_forget()
    except Exception as e:
        print(e)

    projects = get_all_projects()
    for project_path in get_all_project_paths_in_data():
        if project_name in project_path:
            project_path_f.append(project_path)
    if len(project_path_f) == 1:
        folder_data = folder_info_recursive(project_path_f[0], project_name, 150)
    if len(project_path_f) > 1:
        result_label.config(text=f"Proyecto repetido: {project_name} en {project_path_f}.", background='yellow', foreground='black')
        for project in project_path_f:
            folder_data = folder_info_recursive(project, project_name, 50)
    if project_name in projects and folder_data:
        result_label.config(text=f"Proyecto encontrado: {project_name} en {project_path_f[0]}\nPreparado para enviar a Backup.")
        client_type = project_path_f[0].split('/')
        type = client_type[2]
        client = client_type[3]
        send_backup_button = tk.Button(root, text="Enviar a Backup", command=lambda: start_backup(type, client, project_name))
        send_backup_button.pack(pady=5, padx=5, anchor='n')
    if  project_name not in projects:
        result_label.config(text="Proyecto no encontrado.", background='red', foreground='black')
    result_label.pack()

class AutocompleteCombobox(ttk.Combobox):
    shared_valid_client = False
    shared_valid_project = False

    def __init__(self, master, *args, **kwargs):
        ttk.Combobox.__init__(self, master, *args, **kwargs)
        self.name = ""
        self.valid_label = tk.Label(master, text="Name already used in another project", font=('Helvetica', 16), fg="red")
        self.valid_label.pack_forget()  # Initially hide the label
        self.create_button = tk.Button(root)
        # self.bind('<FocusOut>', lambda event: self.validate_entry())  # Bind the <FocusOut> event
        self._valid_items = set()
        self.last_key_release_time = 0

        self.bind('<KeyRelease>', self.handle_keyrelease)

    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list)
        self._hits = []
        self['values'] = self._completion_list

    def autocomplete(self):
        self.position = len(self.get())
        _hits = [item for item in self._completion_list if item.lower().startswith(self.get().lower())]

        self['values'] = _hits
        if _hits:
            # Simulate pressing Down arrow key to show the dropdown
            self.event_generate('<Down>')
        elif not _hits and self.get() == '':
            self.set_completion_list(self._valid_items)
        elif not _hits and self.get() != '':
            self.set_completion_list([])
        # Check if the entered client name is valid
        if self.name == "proyects":
            if self.get() not in self._valid_items:
                self.valid_label.pack_forget()  # Hide the label
            else:
                self.valid_label.pack(side="top")  # Show the label
                self.set_completion_list([])  # Hide dropdown options

    def handle_keyrelease(self, event):
        if event.keysym in ('Up', 'Down', 'Control_R', 'Control_L'):
            return

        # Update the time of the last key release
        self.last_key_release_time = time.time()

        # After 500 milliseconds (0.5 seconds), call the check_autocomplete function
        self.after(500, self.check_autocomplete)
        self.after(500, self.validate_entry)

    def check_autocomplete(self):
        # Check if the time difference is greater than or equal to 0.5 seconds and the dropdown is not active
        if time.time() - self.last_key_release_time >= 0.5:
            self.autocomplete()

    def validate_entry(self):
        # Verificar si el entry tiene un valor válido al perder el foco
        if self.get():
            if self.name == "proyects":
                AutocompleteCombobox.shared_valid_project = True
            else:
                AutocompleteCombobox.shared_valid_client = True
        if AutocompleteCombobox.shared_valid_client and AutocompleteCombobox.shared_valid_project:
            self.create_button.config(state=tk.NORMAL)
        if not self.get():
            return False


class CreateOrderApp:
    def __init__(self) -> None:
        # Menú inicial para elegir la acción a realizar
        self.menu_frame = tk.Frame(root)
        self.menu_frame.pack()

        self.new_project_button = tk.Button(self.menu_frame, text="Crear Nuevo Proyecto", command=self.show_new_project_interface)
        self.new_project_button.pack(side=tk.LEFT)

        self.archive_project_button = tk.Button(self.menu_frame, text="Proyecto Terminado, enviar a Backup", command=self.show_archive_project_interface)
        self.archive_project_button.pack(side=tk.LEFT)

    def show_main_menu(self):
        self.clear_interface()

        # Añadir el logo de Stupendastic al menú principal
        try:
            global logo
            logo = tk.PhotoImage(file=LOGO_PATH)
            label_logo = tk.Label(root, image=logo,height=220, width=1500)
            label_logo.pack(pady=10)  # Añade un poco de espacio vertical (pady) alrededor del logo
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el logo: {e}")

        # Botones del menú principal
        quit_button = tk.Button(root, text="X", command=root.destroy)
        quit_button.pack(side="right", anchor="n")
        new_project_button = tk.Button(root, text="Crear Nuevo Proyecto", command=self.show_new_project_interface)
        new_project_button.pack(pady=10)

        archive_project_button = tk.Button(root, text="Proyecto Terminado, enviar a Backup", command=self.show_archive_project_interface)
        archive_project_button.pack(pady=10)

    def show_new_project_interface(self):
        global logo  # Referencia a la variable global 'logo'
        self.clear_interface()
        # Añadir el logo de Stupendastic
        try:
            # Asegúrate de que la ruta al archivo del logo es accesible y correcta
            logo = tk.PhotoImage(file=LOGO_PATH)
            label_logo = tk.Label(root, image=logo,height=220, width=1500)
            label_logo.pack()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el logo: {e}")



        # Descripción del script
        description_label = tk.Label(root, text="\nEste Script creará carpetas en las siguientes ubicaciones:\nDATA, EDITORES EXTERNOS, FILMMAKERS, CONNECT\n")

        # Añadir menú desplegable con función de autocompletar para el nombre del cliente
        label_client = tk.Label(root, text="Nombre del Cliente:")
        combo_clients = AutocompleteCombobox(root)
        combo_clients.name = "clients"
        combo_clients._valid_items = get_existing_clients()
        combo_clients.set_completion_list(get_existing_clients())

        # Añadir entrada para el nombre del proyecto
        proyectos_path = f"{DATA_PATH}/PROYECTOS"
        proyectos_orders = get_all_orders(proyectos_path)
        seguimiento_path = f"{DATA_PATH}/SEGUIMIENTOS"
        seguimiento_orders = get_all_orders(seguimiento_path)
        all_orders = proyectos_orders + seguimiento_orders

        label_project = tk.Label(root, text="Nombre del Proyecto:")
        entry_project = AutocompleteCombobox(root)
        entry_project.name = "proyects"
        entry_project._valid_items = all_orders
        entry_project.set_completion_list(all_orders)

        # Opciones para el tipo de proyecto, con "SEGUIMIENTOS" seleccionado por defecto
        project_type_var = tk.StringVar(value="SEGUIMIENTOS")
        radio_project = tk.Radiobutton(root, text="Proyecto", variable=project_type_var, value="PROYECTOS")
        radio_follow_up = tk.Radiobutton(root, text="Seguimiento", variable=project_type_var, value="SEGUIMIENTOS")

        # Botón para crear las carpetas
        create_button = entry_project.create_button
        create_button.config(text="Crear Carpetas")
        create_button.config(command=lambda: on_submit(combo_clients, entry_project, project_type_var))
        create_button.config(state=tk.DISABLED)


        def back():
            description_label.destroy()
            label_client.destroy()
            combo_clients.destroy()
            label_project.destroy()
            entry_project.destroy()
            create_button.destroy()
            radio_follow_up.destroy()
            radio_project.destroy()
            label_result.destroy()
            self.show_main_menu()

        # Etiqueta para mostrar el resultado de la operación
        label_result = tk.Label(root, text="")
        label_result.pack()
        back_button = tk.Button(root, text="Back", command=back)
        back_button.pack(side="left", anchor="n")

        description_label.pack()

        label_client.pack()

        combo_clients.pack()

        label_project.pack()

        entry_project.pack()

        radio_follow_up.pack()

        radio_project.pack()

        create_button.pack()


    # Función para mostrar la interfaz de archivo de proyecto
    def show_archive_project_interface(self):
        self.clear_interface()
        global logo  # Referencia a la variable global 'logo'
        try:
            logo = tk.PhotoImage(file=LOGO_PATH)
            label_logo = tk.Label(root, image=logo, bg=background_color,height=220, width=1500)
            label_logo.pack(pady=10)  # Añade un poco de espacio vertical
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el logo: {e}")

        proyectos_path = f"{DATA_PATH}/PROYECTOS"
        proyectos_orders = get_all_orders(proyectos_path)
        seguimiento_path = f"{DATA_PATH}/SEGUIMIENTOS"
        seguimiento_orders = get_all_orders(seguimiento_path)
        all_orders = proyectos_orders + seguimiento_orders

        # Campo de búsqueda
        search_label = tk.Label(root, text="Nombre del Proyecto a Archivar:", bg=background_color)
        search_label.pack(pady=5, padx=5)
        search_entry = AutocompleteCombobox(root)
        search_entry._valid_items = all_orders
        search_entry.set_completion_list(all_orders)
        search_entry.pack(pady=5, padx=5)

        # Botón de búsqueda
        search_button = tk.Button(root, text="Buscar Proyecto", command=lambda: search_project(search_entry.get()))
        search_button.pack(pady=5, padx=5)

        # Resultados de búsqueda
        global result_label
        back_button = tk.Button(root, text="Back", command=self.show_main_menu)
        back_button.pack(side="left", anchor="n")
        result_label = tk.Label(root, text="", bg=background_color)
        result_label.pack(pady=5, padx=5)

    def clear_interface(self):
        for widget in root.winfo_children():
            widget.destroy()

def start_backup(project_type, client_name, project_name):
    ftp_data_project_path  = f"{os.path.join('./FTP 24.7 v2')}/{client_name}/{project_name}"
    folder_info_recursive(ftp_data_project_path, project_name, 150, True)
    if project_type and client_name:
        # Iniciar transferencias paralelas
        if move_project_to_backup_from_data(project_name, client_name):
            if not move_editores_externos_to_backup(project_name, client_name):
                messagebox.showerror("Error", "No se pudo mover la carpeta de EDITORES EXTERNOS.")
        else:
            messagebox.showerror("Error", "No se pudo mover la carpeta de DATA.")
        move_or_delete_filmmakers_folder(project_name, client_name)
    else:
        messagebox.showerror("Error", "No se pudo encontrar detalles del proyecto.")