import Tkinter as tk
import Network
import VisualizerFrame
import Animator


class Visualizer(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        #Vars
        self.statusVar = tk.StringVar()
        self.pathVar = tk.StringVar()
        self.widthVar = tk.IntVar()
        self.heightVar = tk.IntVar()
        self.tVar = tk.StringVar()
        self.iterVar = tk.StringVar()
        self.radiusVar = tk.StringVar()
        self.springVar = tk.StringVar()
        self.statusVar.set("Ready")

        self.widthVar.set(600)
        self.heightVar.set(400)
        self.tVar.set(0.01)
        self.iterVar.set(500)
        self.radiusVar.set(5)
        self.springVar.set(5)


        #Labels
        path = tk.Label(self,text = "Path")
        width = tk.Label(self,text = "Width")
        height = tk.Label(self, text="Height")
        t = tk.Label(self, text="Step size")
        iter = tk.Label(self, text="Iterations")
        radius = tk.Label(self, text="Radius")
        spring = tk.Label(self, text="Spring length (in radius)")
        status = tk.Label(self, textvariable=self.statusVar)
        path.grid(row=0,column=0,sticky="w",pady=5,padx=5)
        width.grid(row=1, column=0, sticky="w", pady=5, padx=5)
        height.grid(row=2, column=0, sticky="w", pady=5, padx=5)
        t.grid(row=3, column=0, sticky="w", pady=5, padx=5)
        iter.grid(row=0, column=2, sticky="w", pady=5, padx=5)
        radius.grid(row=1, column=2, sticky="w", pady=5, padx=5)
        spring.grid(row=2, column=2, sticky="w", pady=5, padx=5)
        status.grid(row=5, column=0,columnspan=4, sticky="ew", pady=5, padx=5)

        #Entry boxes
        pathEntry = tk.Entry(self, textvariable=self.pathVar,justify='center')
        widthEntry = tk.Entry(self, textvariable=self.widthVar,justify='center')
        heightEntry = tk.Entry(self, textvariable=self.heightVar,justify='center')
        tEntry = tk.Entry(self, textvariable=self.tVar,justify='center')
        iterEntry = tk.Entry(self, textvariable=self.iterVar,justify='center')
        radiusEntry = tk.Entry(self, textvariable=self.radiusVar,justify='center')
        springEntry = tk.Entry(self, textvariable=self.springVar,justify='center')
        pathEntry.grid(row=0,column=1,sticky="w",pady=5,padx=5)
        widthEntry.grid(row=1,column=1,sticky="w",pady=5,padx=5)
        heightEntry.grid(row=2,column=1,sticky="w",pady=5,padx=5)
        tEntry.grid(row=3,column=1,sticky="w",pady=5,padx=5)
        iterEntry.grid(row=0,column=3,sticky="w",pady=5,padx=5)
        radiusEntry.grid(row=1,column=3,sticky="w",pady=5,padx=5)
        springEntry.grid(row=2,column=3,sticky="w",pady=5,padx=5)

        #Create the visual Canvas
        self.visualizer = VisualizerFrame.VisualizerFrame(600, 400, bd=2, relief="sunken")
        self.visualizer.grid(row=4, column=0, columnspan=4, pady=5, padx=5, sticky="ew")

        #Buttons
        runButton = tk.Button(self,text="Run",command=self.run)
        runButton.grid(row=6,column=0,columnspan=4,pady=5,padx=5)




    def run(self):
        self.visualizer.canvas.delete("all")
        #Change our status var
        self.statusVar.set("Initializing")

        # Create our network change our visualizers size
        network = Network.Network(self.widthVar.get(), self.heightVar.get(), float(self.springVar.get()))
        self.visualizer.config(width=self.widthVar.get(),height=self.heightVar.get())
        self.visualizer.addNetwork(network)

        #Create our settings dict
        settingsDict = dict()
        settingsDict["path"] = (self.pathVar.get())
        settingsDict["t"] = float(self.tVar.get())
        settingsDict["iter"] = float(self.iterVar.get())
        settingsDict["radius"] = float(self.radiusVar.get())
        settingsDict["spring"] = float(self.springVar.get())
        settingsDict["network"] = network
        settingsDict["visualizer"] = self.visualizer
        settingsDict["statusVar"] = self.statusVar

        #Run our program
        Animator.run(settingsDict)


if __name__ == "__main__":
    root = Visualizer()
    root.mainloop()
    #u"/Users/tobiasfuma/Desktop/FirmenbuchCrawler/Results/20170503_tirol_beauty/network.xlsx"