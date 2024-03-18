import tkinter as tk
from tkinter import scrolledtext

class Gui(tk.Tk):
    def __init__(self, controller, name = "Resizable Chat Interface") -> None:
        super().__init__()
        self.controller = controller

        # Create the main window
        self.title(name)

        # Create a menu bar
        menubar = tk.Menu(self)

        # Create a File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Configure the menu bar
        self.config(menu=menubar)        

        # Create a scrolled text widget for displaying the chat messages (state='disabled')
        self.chat_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=40, height=15, state=tk.NORMAL)
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create a scrolled text widget for displaying the chat messages (state='disabled')
        # self.asd_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=40, height=15, state=tk.NORMAL)
        # self.asd_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create a frame to hold the input area and the send button
        self.input_frame = tk.Frame(self)
        self.input_frame.pack(padx=10, pady=10, fill=tk.X)

        # Create an entry widget for typing messages
        self.entry = tk.Entry(self.input_frame, width=30)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Create a button to send messages
        self.say_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.say_button.pack(side=tk.LEFT, padx=5)

        # Set up the event binding for the Enter key to send messages
        self.bind('<Return>', lambda event=None: self.send_message())

    def write_message(self, message):
        if message:
            self.chat_area.insert(tk.END, message)
            self.entry.delete(0, tk.END)

    def send_message(self):
        self.controller.send_message(self.entry.get())

    def update_chat_display(self, history: str):
        self.asd_area.delete("1.0", tk.END)
        self.asd_area.insert(tk.END, history)
