# -*- coding: utf-8 -*-

import Tkinter as tk
import datetime
import os

class GUI_Results(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Configure main frame
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)

        # StringVars
        self.statusVar = tk.StringVar()
        self.resultsVar = tk.StringVar()

        # Initial statuses
        self.statusVar.set("Retrieving websites")
        self.resultsVar.set("Searching...")

        # Labels
        title = tk.Label(self, bg="white", text="Results")
        resultsLabel = tk.Label(self, bg="white", textvariable=self.resultsVar)
        statusLabel = tk.Label(self, bg="white", textvariable=self.statusVar)
        title.grid(row=0, column=0, columnspan=2, sticky="ew")
        resultsLabel.grid(row=1, column=0, columnspan=2, sticky="ew")
        statusLabel.grid(row=2, column=0, columnspan=2, sticky="ew")

        # Buttons
        openResults = tk.Button(self, width=20, text="Open results", command=self.openResults)
        dataProcessing = tk.Button(self, width=20, text="Process results",
                                   command=lambda: controller.show_frame("GUI_DataProcessing"))
        back = tk.Button(self, width=20, text="Back", command=lambda: controller.show_frame("GUI_Search"))
        openResults.grid(row=3, column=0, columnspan=2, pady=10, padx=10)
        dataProcessing.grid(row=4, column=1, pady=10, padx=10)
        back.grid(row=4, column=0, pady=10, padx=10)

    def updateStatusVar(self, newStatus):
        self.statusVar.set(str(newStatus))
        self.update()

    def updateResultsVar(self, newResults):
        if newResults == 0:
            self.resultsVar.set("No results found.")
        else:
            self.resultsVar.set("Found " + str(newResults) + " companies.")
        self.update()

    def openResults(self):
        frame = self.controller.get_frame("GUI_Search")
        what = frame.industryStringVar.get()
        where = frame.areaStringVar.get()
        filename = datetime.date.today().strftime("%Y%m%d") + "_"+where+"_"+what+".xlsx"
        os.system("open " + filename)
