import tkinter as tk
from tkinter import filedialog
import ntpath
from tkinter import messagebox
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

        self.opened_windows[len(self.opened_windows)] = {
            'index': '!button' + str(len(self.opened_windows) + 1),
            'file_name': 'New File',
            'file_content': '',
            'file_path': None
        }

        self.current_window = len(self.opened_windows) - 1

        self.append_button('New File')

    # append button
    def append_button(self, name):
        button = tk.Button(self.toolbar, text=name,
                           bg=constants.SELECT_BACKGROUND, fg=constants.WHITE_COLOR, relief=tk.FLAT, font=constants.SMALL_FONT, command=lambda index=self.current_window: self.update_window(index))
        button.pack(side=tk.LEFT, padx=3, pady=0)

        for key, window in self.opened_windows.items():
            if key != self.current_window:
                self.toolbar.children[window['index']].config(
                    background=constants.BUTTON_BACKGROUND, foreground=constants.FOREGROUND_COLOR)

    # open a file
    def open(self):
        text_file = filedialog.askopenfile(
            initialdir="/", title="Select file", filetypes=self.file_types)
        self.root.title(ntpath.basename(text_file.name) + " - Text Editor")

        if text_file:
            self.opened_file = text_file.name

        text_file = open(text_file.name, "r")
        content = text_file.read()

        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, content)

        text_file.close()

        self.opened_windows[len(self.opened_windows)] = {
            'index': '!button' + str(len(self.opened_windows) + 1),
            'file_name': ntpath.basename(text_file.name),
            'file_content': content,
            'file_path': text_file.name
        }

        self.current_window = len(self.opened_windows) - 1

        self.append_button(ntpath.basename(text_file.name))

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

        self.toolbar.children[self.opened_windows[self.current_window]['index']].config(
            background=constants.SELECT_BACKGROUND, foreground="#FFFFFF")

        for key, window in self.opened_windows.items():
            if key != self.current_window:
                self.toolbar.children[window['index']].config(
                    background=constants.BUTTON_BACKGROUND, foreground=constants.FOREGROUND_COLOR)

        self.root.title(
            self.opened_windows[self.current_window]['file_name'] + " - Text Editor")

        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(
            tk.END, self.opened_windows[self.current_window]['file_content'])

    # find in file
    def find(self):
        self.find_window = tk.Toplevel(self.root)
        self.find_window.title("Find")
        self.find_window.geometry("250x60")

        self.find_label = tk.Label(self.find_window, text="Find:")
        self.find_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.find_entry = tk.Entry(
            self.find_window, relief=tk.FLAT, background=constants.BUTTON_BACKGROUND)
        self.find_entry.pack(side=tk.LEFT, padx=5, pady=5)

        self.find_button = tk.Button(
            self.find_window, text="Search", command=self.find_text, relief=tk.FLAT, background=constants.BUTTON_BACKGROUND, foreground=constants.FOREGROUND_COLOR)
        self.find_button.pack(side=tk.LEFT, padx=5, pady=5)

    # find text in the text box
    def find_text(self):
        text = self.find_entry.get()
        self.text_box.tag_remove("found", 1.0, tk.END)

        if text:
            start_pos = self.text_box.search(text, 1.0, tk.END)
            while start_pos:
                end_pos = f"{start_pos}+{len(text)}c"
                self.text_box.tag_add("found", start_pos, end_pos)
                start_pos = self.text_box.search(text, end_pos, tk.END)
            self.text_box.tag_config(
                "found", background="yellow")

        self.find_window.protocol("WM_DELETE_WINDOW", self.on_search_close)

    # on search window close
    def on_search_close(self):
        self.text_box.tag_remove("found", 1.0, tk.END)
        self.find_window.destroy()

    # replace in text
    def replace(self):
        self.replace_window = tk.Toplevel(self.root)
        self.replace_window.title("Replace")
        self.replace_window.geometry("420x60")

        self.replace_label = tk.Label(self.replace_window, text="Find:")
        self.replace_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.replace_entry = tk.Entry(
            self.replace_window, relief=tk.FLAT, background=constants.BUTTON_BACKGROUND)
        self.replace_entry.pack(side=tk.LEFT, padx=5, pady=5)

        self.replace_label2 = tk.Label(self.replace_window, text="Replace:")
        self.replace_label2.pack(side=tk.LEFT, padx=5, pady=5)

        self.replace_entry2 = tk.Entry(
            self.replace_window, relief=tk.FLAT, background=constants.BUTTON_BACKGROUND)
        self.replace_entry2.pack(side=tk.LEFT, padx=5, pady=5)

        self.replace_button = tk.Button(
            self.replace_window, text="Go", command=self.replace_text, relief=tk.FLAT, background=constants.BUTTON_BACKGROUND, foreground=constants.FOREGROUND_COLOR)
        self.replace_button.pack(side=tk.LEFT, padx=5, pady=5)

    # replace text
    def replace_text(self):
        text = self.replace_entry.get()
        replace_text = self.replace_entry2.get()

        if text:
            start_pos = self.text_box.search(text, 1.0, tk.END)
            while start_pos:
                end_pos = f"{start_pos}+{len(text)}c"
                self.text_box.delete(start_pos, end_pos)
                self.text_box.insert(start_pos, replace_text)
                start_pos = self.text_box.search(text, end_pos, tk.END)
