import tkinter as tk
from tkinter import filedialog
import ntpath
import helpers.constants as constants


class File:
    def __init__(self, root, text_box, toolbar):
        self.root = root
        self.text_box = text_box
        self.toolbar = toolbar

        self.file_types = (
            ("Text Files", "*.txt"),
            ("Python Files", "*.py"),
            ("All Files", "*.*")
        )

        self.opened_file = None

        self.selected = None

        self.opened_windows = {}
        self.current_window = 0

    # create a new file
    def new(self):
        self.text_box.delete(1.0, tk.END)
        self.root.title("New File - Text Editor")

        self.opened_file = None

        self.opened_windows[self.current_window + 1] = {
            'index': '!button' + str(len(self.opened_windows) + 1),
            'file_name': 'New File',
            'file_content': '',
            'file_path': None
        }

        self.current_window = len(self.opened_windows) - 1

        button = tk.Button(self.toolbar, text="New File",
                           bg=constants.LIGHT_GRAY, fg=constants.FOREGROUND_COLOR, font=constants.SMALL_FONT, command=lambda index=self.current_window: self.update_window(index))
        button.pack(side=tk.LEFT, padx=5, pady=5)

    # open a file
    def open(self):
        self.text_box.delete(1.0, tk.END)

        text_file = filedialog.askopenfile(
            initialdir="/", title="Select file", filetypes=self.file_types)
        self.root.title(ntpath.basename(text_file.name) + " - Text Editor")

        if text_file:
            self.opened_file = text_file.name

        text_file = open(text_file.name, "r")
        content = text_file.read()

        self.text_box.insert(tk.END, content)

        text_file.close()

        self.opened_windows[self.current_window + 1] = {
            'index': '!button' + str(len(self.opened_windows) + 1),
            'file_name': ntpath.basename(text_file.name),
            'file_content': content,
            'file_path': text_file.name
        }

        self.current_window = len(self.opened_windows) - 1

        button = tk.Button(self.toolbar, text=ntpath.basename(text_file.name),
                           bg=constants.LIGHT_GRAY, fg=constants.FOREGROUND_COLOR, font=constants.SMALL_FONT, command=lambda index=self.current_window: self.update_window(index))
        button.pack(side=tk.LEFT, padx=5, pady=5)

    # close the file
    def close(self):
        self.toolbar.children[self.opened_windows[self.current_window]
                              ['index']].pack_forget()
        self.opened_windows.pop(self.current_window)

        for key, window in self.opened_windows.items():
            self.current_window = key
            break

        if len(self.opened_windows) == 0:
            self.root.quit()
            return

        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(
            tk.END, self.opened_windows[self.current_window]['file_content'])

    # save a file
    def save(self):
        if self.opened_file:
            text_file = open(self.opened_file, "w")
            content = self.text_box.get(1.0, tk.END)
            text_file.write(content)
            text_file.close()
        else:
            self.save_as()

    # save a file as
    def save_as(self):
        text_file = filedialog.asksaveasfile(
            mode="w", defaultextension=".*", initialdir="/", title="Save file as", filetypes=self.file_types)
        if text_file:
            self.opened_file = text_file.name
            self.opened_windows[self.current_window]['file_path'] = self.opened_file

            self.root.title(ntpath.basename(text_file.name) + " - Text Editor")

            self.toolbar.children[self.opened_windows[self.current_window]['index']].config(
                text=ntpath.basename(text_file.name))

            text_file = open(text_file.name, "w")
            content = self.text_box.get(1.0, tk.END)
            text_file.write(content)
            text_file.close()

    # cut the text
    def cut_text(self, event):
        if event:
            self.selected = self.root.clipboard_get()
        else:
            if self.text_box.selection_get():
                self.selected = self.text_box.selection_get()
                self.root.clipboard_clear()
                self.root.clipboard_append(self.selected)
                self.text_box.delete(tk.SEL_FIRST, tk.SEL_LAST)

    # paste text
    def paste_text(self, event):
        if event:
            self.selected = self.root.clipboard_get()
        else:
            if self.selected:
                position = self.text_box.index(tk.INSERT)
                self.text_box.insert(position, self.selected)

    # copy text
    def copy_text(self, event):
        if event:
            self.selected = self.root.clipboard_get()

        if self.text_box.selection_get():
            self.selected = self.text_box.selection_get()
            self.root.clipboard_clear()
            self.root.clipboard_append(self.selected)

    # update window
    def update_window(self, index):
        self.current_window = index
        self.opened_file = self.opened_windows[self.current_window]['file_path']

        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(
            tk.END, self.opened_windows[self.current_window]['file_content'])
