# -*- coding: utf-8 -*-
import Tkinter as tk
import tkMessageBox
from threading import Thread
import time
from Crawler import Crawler_controller
from Formater import EnsureFormat

class GUI_Search(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #Configure main frame  
        self.controller = controller         
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)
        self.rowconfigure(3,weight=1)
        #self.rowconfigure(4,weight=1)
        
        #Labels
        title = tk.Label(self,bg="white",text="Search by Industry and/or Area")
        areaLabel = tk.Label(self,bg="white",text="Area:")
        industryLabel = tk.Label(self,bg="white",text="Industry:")
        title.grid(row=0,column=0,columnspan=2,sticky="ew",padx=10,pady=10)
        areaLabel.grid(row=1,column=0,sticky="w",padx=10)
        industryLabel.grid(row=2,column=0,sticky="w",padx=10)
        
        #StringVars
        self.areaStringVar = tk.StringVar()
        self.industryStringVar = tk.StringVar()        
        
        #Entry boxes
        areaEntry = tk.Entry(self,textvariable=self.areaStringVar)
        industryEntry = tk.Entry(self,textvariable=self.industryStringVar)
        areaEntry.grid(row=1,column=1,padx=10)
        industryEntry.grid(row=2,column=1,padx=10)
        
        """#Further criteria frame
        critFrame = tk.Frame(self,bd=2,relief="sunken")
        critFrame.grid(row=3,column=0,columnspan=2,sticky="news",pady=5,padx=5)
        critFrame.columnconfigure(0,weight=1)
        critFrame.columnconfigure(1,weight=1)
        critFrame.rowconfigure(0,weight=1)
        critFrame.rowconfigure(1,weight=1)
        critFrame.rowconfigure(2,weight=1)
        critFrame.rowconfigure(3,weight=1)
        critFrame.rowconfigure(4,weight=1)
        
        #crit - Labels
        tk.Label(critFrame,text="Only include results that have the following data").grid(row=0,column=0,columnspan=2,sticky="ew")
        
        #crit - dict of intvars
        self.critDict = dict()
        self.critDict["URL"]=tk.IntVar()
        self.critDict["Email"]=tk.IntVar()
        self.critDict["Phone"]=tk.IntVar()
        self.critDict["Founding date"]=tk.IntVar()
        self.critDict["Employees"]=tk.IntVar()
        self.critDict["Description"]=tk.IntVar()
        self.critDict["Revenue"]=tk.IntVar()
        self.critDict["Associates"]=tk.IntVar()
        
        #crit - Checkbuttons
        tk.Checkbutton(critFrame, text="URL",variable=self.critDict["URL"]).grid(row=1,column=0,sticky="w")
        tk.Checkbutton(critFrame, text="Email",variable=self.critDict["Email"]).grid(row=2,column=0,sticky="w")
        tk.Checkbutton(critFrame, text="Phone Number",variable=self.critDict["Phone"]).grid(row=3,column=0,sticky="w")
        tk.Checkbutton(critFrame, text="Founding Date",variable=self.critDict["Founding date"]).grid(row=4,column=0,sticky="w")
        tk.Checkbutton(critFrame, text="Employee #",variable=self.critDict["Employees"]).grid(row=1,column=1,sticky="w")
        tk.Checkbutton(critFrame, text="Description",variable=self.critDict["Description"]).grid(row=2,column=1,sticky="w")
        tk.Checkbutton(critFrame, text="Revenue",variable=self.critDict["Revenue"]).grid(row=3,column=1,sticky="w")
        tk.Checkbutton(critFrame, text="Associates",variable=self.critDict["Associates"]).grid(row=4,column=1,sticky="w")
        """
        
        
        #Buttons
        back = tk.Button(self,width=10, text="Back",command=lambda: controller.show_frame("GUI_Main"))
        run = tk.Button(self,width=10, text="Run",command=self.run) 
        back.grid(row=3,column=0,pady=10,padx=10)
        run.grid(row=3,column=1,pady=10,padx=10)
    
    def run(self):
        #Get our set variables
        what = EnsureFormat.ensureUnicode(self.industryStringVar.get())
        where = EnsureFormat.ensureUnicode(self.areaStringVar.get())

        # Check that we entered data in both fields
        if where == "" or what == "":
            tkMessageBox.showinfo("Error", "Enter data for both search fields")

        #Switch frames
        resultFrame = self.controller.get_frame("GUI_Results")
        self.controller.show_frame("GUI_Results")

        #Set initial state of all variables
        resultFrame.statusVar.set("Retrieving websites")
        resultFrame.statusVar.set("Searching...")

        #Run the crawler in a separate thread and make sure we keep updating our page
        t = Thread(target=Crawler_controller.runCrawler, args=(where,what,resultFrame.statusVar,resultFrame.resultsVar))
        t.start()
        while t.isAlive():
            self.update()
            time.sleep(0.1)


            
            

        
        