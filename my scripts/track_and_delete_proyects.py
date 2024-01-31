import os
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def calculate_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)
    return total_size

def list_folders():
    folder_path = filedialog.askdirectory(title="Seleccionar Carpeta Principal")

    if not folder_path:
        return  # El usuario canceló la selección o cerró la ventana

    result_treeview.delete(*result_treeview.get_children())

    try:
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for dirname in dirnames:
                subfolder_path = os.path.join(dirpath, dirname)
                folder_size = calculate_folder_size(subfolder_path)

                if folder_size < 10 * 1024 * 1024:  # 10 MB en bytes
                    result_treeview.insert("", tk.END, values=(subfolder_path, "Borrar"), tags=(subfolder_path,))
                    result_treeview.tag_configure(subfolder_path, background="lightgreen")
    except Exception as e:
        print(f"Error al listar carpetas: {str(e)}")

def delete_folder(selected_item):
    folder_path = result_treeview.item(selected_item, 'values')[0]

    try:
        shutil.rmtree(folder_path)
        result_treeview.delete(selected_item)
    except Exception as e:
        print(f"Error al borrar la carpeta: {str(e)}")

# Crear la ventana principal
root = tk.Tk()
root.title("Listado de Carpetas")

# Botón para listar carpetas
list_button = tk.Button(root, text="Listar Carpetas", command=list_folders)
list_button.pack()

# Treeview para mostrar el listado
result_treeview = ttk.Treeview(root, columns=("Ruta", "Borrar"))
result_treeview.heading("#0", text="Carpeta")
result_treeview.heading("Ruta", text="Ruta")
result_treeview.heading("Borrar", text="Borrar")

# Configurar la acción del botón Borrar en el Treeview
result_treeview.bind("<ButtonRelease-1>", lambda event: delete_folder(result_treeview.selection()[0]) if result_treeview.identify_region(event.x, event.y) == "cell" else None)

# Barra de desplazamiento horizontal
xscrollbar = ttk.Scrollbar(root, orient="horizontal", command=result_treeview.xview)
xscrollbar.pack(side="bottom", fill="x")
result_treeview.configure(xscrollcommand=xscrollbar.set)

result_treeview.pack()

# Iniciar el bucle principal
root.mainloop()
