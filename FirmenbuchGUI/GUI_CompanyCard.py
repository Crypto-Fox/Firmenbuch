import Tkinter as tk

class GUI_CompanyCard(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #Configure the frame
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.rowconfigure(8, weight=1)
        self.rowconfigure(9, weight=1)
        self.rowconfigure(10, weight=1)
        self.rowconfigure(11, weight=1)
        self.rowconfigure(12, weight=1)
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)

        #StringVars
        self.nameVar = tk.StringVar()
        self.employeeVar = tk.StringVar()
        self.revenueVar = tk.StringVar()
        self.foundingVar = tk.StringVar()
        self.progressVar = tk.StringVar()

        #Labels
        titleLabel = tk.Label(self,text="Company Profile")
        nameLabel = tk.Label(self, text="Name:")
        employeeLabel = tk.Label(self, text="Employee #")
        revenueLabel = tk.Label(self, text="Revenue")
        foundingLabel = tk.Label(self, text="Founding date")
        descLabel = tk.Label(self, text="Description")
        associateLabel = tk.Label(self, text="Associates")
        titleLabel.grid(row=0,column=0,columnspan=2,sticky="ew",pady=10,padx=5)
        nameLabel.grid(row=2, column=0, sticky="w",padx=5)
        employeeLabel.grid(row=3, column=0, sticky="w",padx=5)
        revenueLabel.grid(row=4, column=0, sticky="w",padx=5)
        foundingLabel.grid(row=5, column=0, sticky="w",padx=5)
        descLabel.grid(row=6, column=0, columnspan=2, sticky="ew",padx=5)
        associateLabel.grid(row=8, column=0, columnspan=2, sticky="ew",padx=5)

        #Entry boxes
        nameEntry = tk.Entry(self,textvariable=self.nameVar)
        employeeEntry = tk.Entry(self, textvariable=self.nameVar)
        revenueEntry = tk.Entry(self, textvariable=self.nameVar)
        foundingEntry = tk.Entry(self, textvariable=self.nameVar)
        nameEntry.grid(row=2, column=1, sticky="w",padx=5)
        employeeEntry.grid(row=3, column=1, sticky="w",padx=5)
        revenueEntry.grid(row=4, column=1, sticky="w",padx=5)
        foundingEntry.grid(row=5, column=1, columnspan=2, sticky="w",padx=5)


        #Buttons
        webButton = tk.Button(self,text="Open company website")
        firmButton = tk.Button(self,text="Open FirmenABC website")
        removeButton = tk.Button(self,text="Remove")
        keepButton = tk.Button(self,text="Keep")
        webButton.grid(row=10, column=0,columnspan=2, padx=5)
        firmButton.grid(row=11, column=0,columnspan=2 , padx=5)
        removeButton.grid(row=12, column=0,sticky="ew", padx=5)
        keepButton.grid(row=12, column=1, sticky="ew", padx=5)

        #Scrollable Text Box
        #Create the frames
        descText = tk.Frame(self,width=350,height=150)
        descText.grid(row=7,column=0,columnspan=2,sticky="news")
        #ensure a consistent GUI size
        descText.grid_propagate(False)
        #implement stretchability
        descText.grid_rowconfigure(0, weight=1)
        descText.grid_columnconfigure(0, weight=1)

        #create a Text widget
        self.descBox = tk.Text(descText, borderwidth=3, relief="sunken")
        self.descBox.config(font=("consolas", 12), undo=True, wrap='word')
        self.descBox.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        #create a Scrollbar and associate it with txt
        scrollb1 = tk.Scrollbar(descText, command=self.descBox.yview)
        scrollb1.grid(row=0, column=1, sticky='nsew')
        self.descBox['yscrollcommand'] = scrollb1.set

        # Create the frames
        associateText = tk.Frame(self, width=350, height=150)
        associateText.grid(row=9, column=0, columnspan=2, sticky="news")
        # ensure a consistent GUI size
        associateText.grid_propagate(False)
        # implement stretchability
        associateText.grid_rowconfigure(0, weight=1)
        associateText.grid_columnconfigure(0, weight=1)

        # create a Text widget
        self.associateBox = tk.Text(associateText, borderwidth=3, relief="sunken")
        self.associateBox.config(font=("consolas", 12), undo=True, wrap='word')
        self.associateBox.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        # create a Scrollbar and associate it with txt
        scrollb = tk.Scrollbar(associateText, command=self.associateBox.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.associateBox['yscrollcommand'] = scrollb.set


if __name__ == "__main__":
    filename ="20170411_tirol_security.xlsx"
    app = GUI_CompanyCard()
    app.mainloop()
