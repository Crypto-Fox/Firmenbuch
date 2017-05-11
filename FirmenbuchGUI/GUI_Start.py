# -*- coding: utf-8 -*-
import Tkinter as tk
from GUI_Main import GUI_Main
from GUI_Search import GUI_Search
from GUI_DataProcessing import GUI_DataProcessing
from GUI_Results import GUI_Results
 
TITLE_FONT = ("Helvetica", 18, "bold")

class GUI_Start(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.grid(row=0,column=0,sticky="news")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (GUI_Main,GUI_Search,GUI_DataProcessing,GUI_Results):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("GUI_Main")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        frame.update()
    
    def get_frame(self,page_name):
        frame = self.frames[page_name]
        return frame
    
    def quit(self):
        self.destroy()

if __name__ == "__main__":
    app = GUI_Start()
    app.mainloop()	
