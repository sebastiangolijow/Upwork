import os
import tkinter as tk
from tkinter import ttk


class AutocompleteEntry(ttk.Combobox):
    def __init__(self, master, label_text, *args, **kwargs):
        ttk.Combobox.__init__(self, master, *args, **kwargs)
        self.valid_label = tk.Label(master, text="", font=('Helvetica', 8))
        self._grid_info = {'row': 0, 'column': 0}  # Default values for row and column
        self._valid_items = set()

        # Add label
        self.label = tk.Label(master, text=label_text, font=('Helvetica', 10))
        self.label.grid(row=self._grid_info['row'], column=self._grid_info['column'], padx=5, pady=5, sticky='n')

    def grid(self, *args, **kwargs):
        ttk.Combobox.grid(self, *args, **kwargs)
        self._grid_info = self.grid_info()
        self.valid_label.grid(row=self._grid_info['row'] - 1, column=self._grid_info['column'], padx=5, pady=5, sticky='n')
        self.label.grid(row=self._grid_info['row'], column=self._grid_info['column'], padx=5, pady=5, sticky='w')




    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list)
        self._hits = []
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self['values'] = self._completion_list

    def read_valid_items(self, file_path):
        try:
            with open(file_path, "r") as file:
                self._valid_items = set(file.read().split(', '))
        except FileNotFoundError:
            print(f"File not found: {file_path}")

    def validate_project_name(self):
        project_folder = "projects"  # Adjust the folder path as needed

        try:
            # Get a list of folder names inside the "projects" folder
            folder_names = [name for name in os.listdir(project_folder) if os.path.isdir(os.path.join(project_folder, name))]
        except FileNotFoundError:
            print(f"Folder not found: {project_folder}")
            return

        # Validate the entered project name against the list of folder names
        if self.get() not in folder_names:
            self.valid_label.config(text="Invalid Project", fg="red")
        else:
            self.valid_label.config(text="Valid Project", fg="green")

    def autocomplete(self, delta=0):
        if delta:
            self.delete(0, tk.END)
        else:
            self.position = len(self.get())

        _hits = []
        for item in self._completion_list:
            if item.lower().startswith(self.get().lower()):
                _hits.append(item)

        self._hits = _hits
        self['values'] = _hits

        if _hits:
            # Simulate pressing Down arrow key to show the dropdown
            self.event_generate('<Down>')
        else:
            self.set_completion_list([])

        # Check if the entered client name is valid
        if self.get() not in self._valid_items:
            self.valid_label.config(text="Valid", fg="green")
        else:
            self.valid_label.config(text="Invalid", fg="red")


    def handle_keyrelease(self, event):
        if event.keysym in ('Up', 'Down', 'Control_R', 'Control_L', 'Return'):
            return

        self.autocomplete()

# Sample projects and clients
projects = ['ProjectA', 'Test', 'Upwork', 'Filmmaker']
clients = ['ClientX', 'ClientY', 'ClientZ']

# Create the main window
root = tk.Tk()
root.title("Autocomplete Demo")

# Create AutocompleteEntry for projects
project_entry = AutocompleteEntry(root, "Project Name")
project_entry.grid(row=1, column=0, padx=10, pady=10)
project_entry.set_completion_list(projects)
project_entry.validate_project_name()  # Call the validation method initially

# Create AutocompleteEntry for clients
client_entry = AutocompleteEntry(root, "Client Name")
client_entry.grid(row=3, column=0, padx=10, pady=10)
client_entry.read_valid_items("clients_names.txt")  # Read valid client names from file
client_entry.set_completion_list(clients)

# Run the main loop
root.mainloop()
