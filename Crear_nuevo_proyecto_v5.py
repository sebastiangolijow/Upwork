import logging
import os
import shutil
import time
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from models.models import CreateOrderApp
from models.models import root


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


#PARTE GRÁFICA___________________________

# Configuración de la ventana principal
root.title("Inicio/Final de Proyecto")
root.geometry("700x600")  # Puedes ajustar el tamaño según tus necesidades
background_color = "#1063FF"
create_app = CreateOrderApp()
create_app.show_main_menu()
create_app.show_new_project_interface()

# Función para mostrar la interfaz de archivo de proyecto
create_app.show_archive_project_interface()
create_app.clear_interface()
create_app.show_main_menu()

# Iniciar la aplicación
root.mainloop()