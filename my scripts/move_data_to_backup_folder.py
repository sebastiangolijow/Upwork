import os
import shutil

def move_data_to_backup():
    data_folder_path = input("Ingrese la ruta completa de la carpeta DATA: ")

    if not os.path.exists(data_folder_path):
        print("La carpeta DATA no existe.")
        return

    backup_folder_path = os.path.join(data_folder_path, "Backup")
    external_editors_folder = os.path.join(data_folder_path, "Editores Externos")

    try:
        # Crear la carpeta Backup si no existe
        os.makedirs(backup_folder_path, exist_ok=True)

        # Mover el contenido de DATA a Backup
        for item in os.listdir(data_folder_path):
            item_path = os.path.join(data_folder_path, item)
            if os.path.isfile(item_path):
                shutil.move(item_path, backup_folder_path)

        # Mover la carpeta de Editores Externos a Backup
        shutil.move(external_editors_folder, backup_folder_path)

        print("Movimiento exitoso.")
    except Exception as e:
        print(f"Error durante el movimiento: {str(e)}")

# Llamar a la función para mover los datos a la carpeta Backup
move_data_to_backup()
