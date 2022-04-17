from cmath import exp
import tkinter as tk
import helpers.constants as constants
from core.file import File


class App:
    def __init__(self):
        # create the main window
        self.root = tk.Tk()
        self.root.title(constants.APP_NAME)
        self.root.geometry("1200x660")

        # create the toolbar
        self.toolbar = self.create_toolbar_frame()

        # create the main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=2)

        # create the scrollbar
        self.text_scrollbar = tk.Scrollbar(self.main_frame)
        self.text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # create the text box
        self.text_box = tk.Text(self.main_frame, width=220, height=55, font=constants.DEFAULT_FONT, selectbackground=constants.SELECT_BACKGROUND,
                                selectforeground=constants.FOREGROUND_COLOR, borderwidth=0, undo=True, yscrollcommand=self.text_scrollbar.set, relief=tk.FLAT)
        self.text_box.pack(fill=tk.BOTH, expand=True)

        # configure the scrollbar
        self.text_scrollbar.config(command=self.text_box.yview)

        # create the menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # define the file menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)

        # define the edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)

        # define statistics
        statistics = {
            "symbols": 0,
            "lines": 0,
            "letters": 0,
            "words": 0,
            "sentences": 0,
            "paragraphs": 0
        }

        stats_text = ""
        for key, value in statistics.items():
            stats_text += f"{key.capitalize()}: {value} | "

        # add the statistics bar
        self.statistics_bar = tk.Label(
            self.root, text=stats_text, relief=tk.FLAT, anchor=tk.SW, padx=5, background=constants.LIGHT_GRAY, foreground=constants.FOREGROUND_COLOR)
        self.statistics_bar.place(
            relx=1.0, rely=1.0, x=-2, y=-2, anchor=tk.SE, relwidth=1.0)

        # create the file object
        self.file = File(self.root, self.text_box, self.toolbar)

    # run the app
    def run(self):
        # create the menu
        self.menu()

        # define the first opened window
        self.file.opened_windows[0] = {
            'index': '!button',
            'file_name': 'Untitled',
            'file_content': self.text_box.get("1.0", tk.END),
            'file_path': None
        }

        # create the toolbar buttons
        self.toolbar_buttons()

        # bind keyboard events
        self.bind_events()

        # main loop
        self.root.mainloop()

    # create toolbar frame
    def create_toolbar_frame(self):
        toolbar_frame = tk.Frame(self.root, bg=constants.LIGHT_GRAY)
        toolbar_frame.pack(side=tk.TOP, fill=tk.X)

        return toolbar_frame

    # configure the menu
    def menu(self):
        # create the file menu
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # configure the file menu
        self.file_menu.add_command(
            label="New", command=self.file.new, accelerator="Ctrl+N")
        self.file_menu.add_command(
            label="Open", command=self.file.open, accelerator="Ctrl+O")
        self.file_menu.add_command(
            label="Close", command=self.file.close, accelerator="Ctrl+W")
        self.file_menu.add_command(
            label="Save", command=self.file.save, accelerator="Ctrl+S")
        self.file_menu.add_command(
            label="Save As", command=self.file.save_as, accelerator="Ctrl+Shift+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.destroy)

        # create the edit menu
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # configure the edit menu
        self.edit_menu.add_command(
            label="Undo", command=self.text_box.edit_undo, accelerator="Ctrl+Z")
        self.edit_menu.add_command(
            label="Redo", command=self.text_box.edit_redo, accelerator="Ctrl+Y")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(
            label="Cut", command=lambda: self.file.cut_text(False), accelerator="Ctrl+X")
        self.edit_menu.add_command(
            label="Copy", command=lambda: self.file.copy_text(False), accelerator="Ctrl+C")
        self.edit_menu.add_command(
            label="Paste", command=lambda: self.file.paste_text(False), accelerator="Ctrl+V")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All")
        self.edit_menu.add_command(
            label="Find", command=self.file.find, accelerator="Ctrl+F")
        self.edit_menu.add_command(
            label="Replace", command=self.file.replace, accelerator="Ctrl+H")

    # draw toolbar button
    def draw_button(self, button_text, bg, fg):
        # create the button
        button = tk.Button(self.toolbar, text=button_text,
                           bg=bg, fg=fg, relief=tk.FLAT, font=constants.SMALL_FONT, command=lambda index=0: self.file.update_window(index))

        # add the button to the toolbar
        button.pack(side=tk.LEFT, padx=3, pady=0)

    # create the toolbar buttons
    def toolbar_buttons(self):
        for key, window in self.file.opened_windows.items():
            self.draw_button(
                window['file_name'], constants.SELECT_BACKGROUND, constants.WHITE_COLOR)

    # count letters
    def count_letters(self, text):
        letters = 0
        for char in text:
            if char.isalpha():
                letters += 1
        return letters

    # count symbols
    def count_symbols(self, text):
        symbols = 0
        for char in text:
            if char.isalpha() == False and char.isdigit() == False:
                symbols += 1
        return symbols

    # update the statistics
    def update(self, event):
        # get the text
        text = self.text_box.get(1.0, tk.END)

        # get the number of lines
        lines = text.count("\n")

        # get the number of words
        words = len(text.split())

        # get the number of sentences
        sentences = len(text.split("."))

        # get the number of symbols
        symbols = self.count_symbols(text)

        # get the number of letters
        letters = self.count_letters(text)

        # get the number of paragraphs
        paragraphs = text.count("\n\n")

        # update the statistics
        statistics = {
            "symbols": symbols,
            "lines": lines,
            "letters": letters,
            "words": words,
            "sentences": sentences,
            "paragraphs": paragraphs
        }

        stats_text = ""
        for key, value in statistics.items():
            stats_text += f"{key.capitalize()}: {value} | "

        # update the statistics bar
        self.statistics_bar.config(text=stats_text)

        # update file content
        self.file.opened_windows[self.file.current_window]['file_content'] = self.text_box.get(
            1.0, tk.END)

    # bind the events
    def bind_events(self):
        self.root.bind("<Control-n>", lambda event: self.file.new())
        self.root.bind("<Control-o>", lambda event: self.file.open())
        self.root.bind("<Control-s>", lambda event: self.file.save())
        self.root.bind("<Control-Shift-S>", lambda event: self.file.save_as())

        self.root.bind("<Control-x>", lambda event: self.file.cut_text(event))
        self.root.bind("<Control-c>", lambda event: self.file.copy_text(event))
        self.root.bind(
            "<Control-v>", lambda event: self.file.paste_text(event))

        self.root.bind("<Control-w>", lambda event: self.file.close())

        self.root.bind("<Control-f>", lambda event: self.file.find())
        self.root.bind("<Control-h>", lambda event: self.file.replace())

        self.root.bind("<KeyPress>", self.update)
        #self.root.bind("<KeyRelease>", self.update_statistics)
