import tkinter as tk
import time
import datetime

class Example(tk.LabelFrame):
    def __init__(self, *args, **kwargs):
        tk.LabelFrame.__init__(self, *args, **kwargs)
        data =[{'folder_name': 'Proyecto', 'is_empty': False, 'file_count': 0, 'last_modified_date': datetime.datetime(2024, 2, 4, 20, 17, 38, 34486), 'project_path': './DATA/PROYECTOS/1770 Films/Hostalric/Proyecto'}, {'folder_name': 'Proyecto/Adobe Premiere Pro Auto-Save', 'is_empty': False, 'file_count': 2, 'last_modified_date': datetime.datetime(2024, 2, 4, 19, 32, 5, 966297), 'project_path': './DATA/PROYECTOS/1770 Films/Hostalric/Proyecto/Adobe Premiere Pro Auto-Save'}, {'folder_name': 'Proyecto/Adobe Premiere Pro Captured Audio', 'is_empty': True, 'file_count': 0, 'last_modified_date': datetime.datetime(2024, 2, 2, 17, 50, 8, 229196), 'project_path': './DATA/PROYECTOS/1770 Films/Hostalric/Proyecto/Adobe Premiere Pro Captured Audio'}, {'folder_name': 'Material', 'is_empty': True, 'file_count': 0, 'last_modified_date': datetime.datetime(2024, 2, 2, 17, 50, 8, 228571), 'project_path': './DATA/PROYECTOS/1770 Films/Hostalric/Material'}, {'folder_name': 'Material/Dron', 'is_empty': True, 'file_count': 0, 'last_modified_date': datetime.datetime(2024, 2, 2, 17, 50, 8, 227031), 'project_path': './DATA/PROYECTOS/1770 Films/Hostalric/Material/Dron'}, {'folder_name': 'Material/SD1', 'is_empty': True, 'file_count': 0, 'last_modified_date': datetime.datetime(2024, 2, 2, 17, 50, 8, 227481), 'project_path': './DATA/PROYECTOS/1770 Films/Hostalric/Material/SD1'}, {'folder_name': 'Material/SD6', 'is_empty': True, 'file_count': 0, 'last_modified_date': datetime.datetime(2024, 2, 2, 17, 50, 8, 228567), 'project_path': './DATA/PROYECTOS/1770 Films/Hostalric/Material/SD6'}, {'folder_name': 'Material/SD5', 'is_empty': True, 'file_count': 0, 'last_modified_date': datetime.datetime(2024, 2, 2, 17, 50, 8, 228333), 'project_path': './DATA/PROYECTOS/1770 Films/Hostalric/Material/SD5'}, {'folder_name': 'Material/SD2', 'is_empty': True, 'file_count': 0, 'last_modified_date': datetime.datetime(2024, 2, 2, 17, 50, 8, 227709), 'project_path': './DATA/PROYECTOS/1770 Films/Hostalric/Material/SD2'}, {'folder_name': 'Material/SD3', 'is_empty': True, 'file_count': 0, 'last_modified_date': datetime.datetime(2024, 2, 2, 17, 50, 8, 227920), 'project_path': './DATA/PROYECTOS/1770 Films/Hostalric/Material/SD3'}, {'folder_name': 'Material/SD4', 'is_empty': True, 'file_count': 0, 'last_modified_date': datetime.datetime(2024, 2, 2, 17, 50, 8, 228134), 'project_path': './DATA/PROYECTOS/1770 Films/Hostalric/Material/SD4'}, {'folder_name': 'Material/Musica', 'is_empty': True, 'file_count': 0, 'last_modified_date': datetime.datetime(2024, 2, 2, 17, 50, 8, 227250), 'project_path': './DATA/PROYECTOS/1770 Films/Hostalric/Material/Musica'}]

        self.grid_columnconfigure(1, weight=1)
        tk.Label(self, text="folder_name", anchor="w").grid(row=0, column=0, sticky="ew")
        tk.Label(self, text="is_empty", anchor="w").grid(row=0, column=1, sticky="ew")
        tk.Label(self, text="file_count", anchor="w").grid(row=0, column=2, sticky="ew")
        tk.Label(self, text="last_modified_date", anchor="w").grid(row=0, column=3, sticky="ew")
        tk.Label(self, text="project_path", anchor="w").grid(row=0, column=3, sticky="ew")

        row = 1
        for item in data:
            nr_label = tk.Label(self, text=item['folder_name'], anchor="w")
            name_label = tk.Label(self, text=item['is_empty'], anchor="w")
            name_label = tk.Label(self, text=item['file_count'], anchor="w")
            name_label = tk.Label(self, text=item['last_modified_date'], anchor="w")
            action_button = tk.Button(self, text="Delete", command=lambda: self.delete(item['project_path']))


            nr_label.grid(row=row, column=0, sticky="ew")
            name_label.grid(row=row, column=1, sticky="ew")
            action_button.grid(row=row, column=3, sticky="ew")

            row += 1

    def delete(self, nr):
        print( "deleting...nr=", nr)

if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(side="top", fill="both", expand=True, padx=10, pady=10)
    root.mainloop()