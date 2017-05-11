import Tkinter as tk


class GUI_DataProcessing(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Configure main frame
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        # Labels
        title = tk.Label(self, bg="white", text="Welcome to the Firmenbuch Webcrawler")
        title.grid(row=0, column=0, sticky="ew")

        # Buttons
        search = tk.Button(self, width=30, bg="skyblue", text="Search",
                           command=lambda: controller.show_frame("GUI_Search"))
        dataProcessing = tk.Button(self, width=30, bg="skyblue", text="Process existing data",
                                   command=lambda: controller.show_frame("GUI_DataProcessing"))
        exit = tk.Button(self, width=30, bg="skyblue", text="Exit", command=parent.quit)
        search.grid(row=1, column=0, pady=10, padx=10)
        dataProcessing.grid(row=2, column=0, pady=10, padx=10)
        exit.grid(row=3, column=0, pady=10, padx=10)
