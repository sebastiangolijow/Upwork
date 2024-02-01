import logging
import os
import shutil
import time
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


# Lo que falta por hacer es lo siguiente:
# Filmmakers: comprobar si la carpeta pesa más de 10mb y en el caso de que no, borrar el proyecto
# Mover DATA a la carpeta de Backup y una vez se haya movido, mover a su interior la carpeta de Editores Externos
# Mejorar el listado de los proyectos y de los clientes, para que sea un autocompletado mientras escribes
# Crear un botón que muestre los proyectos inactivos por orden de inactividad y con su ruta completa y última interacción (obviando 0. Graphic)
# Crear un Bat o parecido para que se pueda abrir la aplicación fácilmente
# Crear un apartado en cerra proyecto que te dé los 24.7 con las fotos más recientes más tardías y ordenarlo de más antiguo a más nuevo y con la ruta.
# Opción Añadir/Borrar 24.7. Que liste los proyectos de 247 activos y cree el Scheduler automático
# Cerrar 247. Borrar los archivos del NAS y mover de pestaña el proyecto en el SpreedSheet
# Que se pueda ver la última foto recibida de un proyecto y ordenarlo cronológicamente

# Rutas de las carpetas destino
# BACKUP_PATH = "/Users/arnau/Stupendastic Dropbox/Admin Stupendastic/Dropbox-Stupendastic/0. Scripts/Manual/Crear_nuevo_proyecto/Pruebas/Enviar a Backup"
BACKUP_PATH = "./BACKUP"
# DATA_PATH = "/Users/arnau/Stupendastic Dropbox/Admin Stupendastic/Dropbox-Stupendastic/0. Scripts/Manual/Crear_nuevo_proyecto/Pruebas/DATA"
DATA_PATH = "./Pruebas/DATA"
# EDITORES_EXTERNOS_PATH = "/Users/arnau/Stupendastic Dropbox/Admin Stupendastic/Dropbox-Stupendastic/0. Scripts/Manual/Crear_nuevo_proyecto/Pruebas/EDITORES EXTERNOS"
EDITORES_EXTERNOS_PATH = "./Pruebas/EDITORES EXTERNOS"
# FILMMAKERS_PATH = "/Users/arnau/Stupendastic Dropbox/Admin Stupendastic/Dropbox-Stupendastic/0. Scripts/Manual/Crear_nuevo_proyecto/Pruebas/FILMMAKERS"
FILMMAKERS_PATH = "./Pruebas/FILMMAKERS"

# CONNECT_PATH = "/Users/arnau/Stupendastic Dropbox/Admin Stupendastic/Dropbox-Stupendastic/0. Scripts/Manual/Crear_nuevo_proyecto/Pruebas/CONNECT"
CONNECT_PATH = "./Pruebas/CONNECT"
# PLANTILLA_PATH = "/Users/arnau/Stupendastic Dropbox/Admin Stupendastic/Dropbox-Stupendastic/0. Scripts/Manual/Crear_nuevo_proyecto/Plantillas carpetas para copiar"
PLANTILLA_PATH = "./Plantillas carpetas para copiar"
# LOGO_PATH = "/Users/arnau/Stupendastic Dropbox/Admin Stupendastic/Dropbox-Stupendastic/0. Scripts/Manual/Crear_nuevo_proyecto/Stpdn_Logos_Color en tamaño pequeño.png"
LOGO_PATH = "./Stpdn_Logos_Color.png"

logo = None

class AutocompleteCombobox(ttk.Combobox):
    def __init__(self, master, *args, **kwargs):
        ttk.Combobox.__init__(self, master, *args, **kwargs)
        self.name = ""
        self.valid_label = tk.Label(master, text="Name already used in another project", font=('Helvetica', 8), fg="red")
        self.valid_label.pack_forget()  # Initially hide the label
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
        elif not _hits:
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

    def check_autocomplete(self):
        # Check if the time difference is greater than or equal to 0.5 seconds and the dropdown is not active
        if time.time() - self.last_key_release_time >= 0.5:
            self.autocomplete()


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


def get_all_projects():
    projects = []
    for tipo in ["PROYECTOS", "SEGUIMIENTOS"]:
        project_path = os.path.join(DATA_PATH, tipo)
        for client in os.listdir(project_path):
            client_path = os.path.join(project_path, client)
            if os.path.isdir(client_path):
                projects.extend(os.listdir(client_path))
    return sorted(set(projects))

def search_project(project_name):
    projects = get_all_projects()
    if project_name in projects:
        result_label.config(text=f"Proyecto encontrado: {project_name}\nPreparado para enviar a Backup.")
        send_backup_button = tk.Button(root, text="Enviar a Backup", command=lambda: start_backup(project_name))
        send_backup_button.pack(pady=5, padx=5)
    else:
        result_label.config(text="Proyecto no encontrado.")




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


#PARTE GRÁFICA___________________________

# Configuración de la ventana principal
root = tk.Tk()
root.title("Inicio/Final de Proyecto")
root.geometry("700x600")  # Puedes ajustar el tamaño según tus necesidades
background_color = "#1063FF"
#root.configure(bg=background_color)

def show_main_menu():
    clear_interface()

    # Añadir el logo de Stupendastic al menú principal
    try:
        global logo
        logo = tk.PhotoImage(file=LOGO_PATH)
        label_logo = tk.Label(root, image=logo)
        label_logo.pack(pady=10)  # Añade un poco de espacio vertical (pady) alrededor del logo
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el logo: {e}")

    # Botones del menú principal
    new_project_button = tk.Button(root, text="Crear Nuevo Proyecto", command=show_new_project_interface)
    new_project_button.pack(pady=10)

    archive_project_button = tk.Button(root, text="Proyecto Terminado, enviar a Backup", command=show_archive_project_interface)
    archive_project_button.pack(pady=10)



def show_new_project_interface():
    global logo  # Referencia a la variable global 'logo'
    clear_interface()

    # Añadir el logo de Stupendastic
    try:
        # Asegúrate de que la ruta al archivo del logo es accesible y correcta
        logo = tk.PhotoImage(file=LOGO_PATH)
        label_logo = tk.Label(root, image=logo)
        label_logo.pack()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el logo: {e}")



    # Descripción del script
    description_label = tk.Label(root, text="\nEste Script creará carpetas en las siguientes ubicaciones:\nDATA, EDITORES EXTERNOS, FILMMAKERS, CONNECT\n")
    description_label.pack()

    # Añadir menú desplegable con función de autocompletar para el nombre del cliente
    label_client = tk.Label(root, text="Nombre del Cliente:")
    label_client.pack()
    combo_clients = AutocompleteCombobox(root)
    combo_clients.name = "clients"
    combo_clients._valid_items = get_existing_clients()
    combo_clients.set_completion_list(get_existing_clients())
    combo_clients.pack()

    # Añadir entrada para el nombre del proyecto
    proyectos_path = "./Pruebas/DATA/PROYECTOS"
    proyectos_orders = get_all_orders(proyectos_path)
    seguimiento_path = "./Pruebas/DATA/SEGUIMIENTOS"
    seguimiento_orders = get_all_orders(seguimiento_path)
    all_orders = proyectos_orders + seguimiento_orders

    label_project = tk.Label(root, text="Nombre del Proyecto:")
    label_project.pack()
    entry_project = AutocompleteCombobox(root)
    entry_project.name = "proyects"
    entry_project._valid_items = all_orders
    entry_project.set_completion_list(all_orders)
    entry_project.pack()

    # Opciones para el tipo de proyecto, con "SEGUIMIENTOS" seleccionado por defecto
    project_type_var = tk.StringVar(value="SEGUIMIENTOS")
    radio_project = tk.Radiobutton(root, text="Proyecto", variable=project_type_var, value="PROYECTOS")
    radio_project.pack()
    radio_follow_up = tk.Radiobutton(root, text="Seguimiento", variable=project_type_var, value="SEGUIMIENTOS")
    radio_follow_up.pack()

    # Botón para crear las carpetas
    create_button = tk.Button(root, text="Crear Carpetas", command= lambda: on_submit(combo_clients, entry_project, project_type_var))

    create_button.pack()

    # Etiqueta para mostrar el resultado de la operación
    label_result = tk.Label(root, text="")
    label_result.pack()



# Función para mostrar la interfaz de archivo de proyecto
def show_archive_project_interface():
    clear_interface()
    global logo  # Referencia a la variable global 'logo'
    try:
        logo = tk.PhotoImage(file=LOGO_PATH)
        label_logo = tk.Label(root, image=logo, bg=background_color)
        label_logo.pack(pady=10)  # Añade un poco de espacio vertical
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el logo: {e}")

    # Campo de búsqueda
    search_label = tk.Label(root, text="Nombre del Proyecto a Archivar:", bg=background_color)
    search_label.pack(pady=5, padx=5)
    search_entry = tk.Entry(root)
    search_entry.pack(pady=5, padx=5)

    # Botón de búsqueda
    search_button = tk.Button(root, text="Buscar Proyecto", command=lambda: search_project(search_entry.get()))
    search_button.pack(pady=5, padx=5)

    # Resultados de búsqueda
    global result_label
    result_label = tk.Label(root, text="", bg=background_color)
    result_label.pack(pady=5, padx=5)

def clear_interface():
    for widget in root.winfo_children():
        widget.destroy()



# Menú inicial para elegir la acción a realizar
menu_frame = tk.Frame(root)
menu_frame.pack()

new_project_button = tk.Button(menu_frame, text="Crear Nuevo Proyecto", command=show_new_project_interface)
new_project_button.pack(side=tk.LEFT)

archive_project_button = tk.Button(menu_frame, text="Proyecto Terminado, enviar a Backup", command=show_archive_project_interface)
archive_project_button.pack(side=tk.LEFT)

# Mostrar el menú principal cuando se inicia la aplicación
show_main_menu()

# Iniciar la aplicación
root.mainloop()