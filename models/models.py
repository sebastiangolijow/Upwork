import logging
import os
import shutil
import time
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

root = tk.Tk()

class AutocompleteCombobox(ttk.Combobox):
    shared_valid_client = False
    shared_valid_project = False

    def __init__(self, master, *args, **kwargs):
        ttk.Combobox.__init__(self, master, *args, **kwargs)
        self.name = ""
        self.valid_label = tk.Label(master, text="Name already used in another project", font=('Helvetica', 8), fg="red")
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

