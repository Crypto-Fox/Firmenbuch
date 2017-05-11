import Tkinter as tk
import tkMessageBox
import Animator


class VisualizerFrame(tk.Frame):
    def __init__(self, width, height, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.canvas = tk.Canvas(self, width=width, height=height, borderwidth=0, highlightthickness=0, bg="white")
        self.canvas.grid()
        self._drag_data = {"x": 0, "y": 0, "item": None}

    def addNetwork(self,network):
        self.network = network


    def createNode(self, x, y, r, **kwargs):
        a = self.canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)
        self.canvas.tag_bind(a,'<Double-Button-1>', self.clickOnObject)
        self.canvas.tag_bind(a, "<ButtonPress-1>", self.on_token_press)
        self.canvas.tag_bind(a, "<ButtonRelease-1>", self.on_token_release)
        self.canvas.tag_bind(a, "<B1-Motion>", self.on_token_motion)

    def createEdge(self,x0,y0,x1,y1,tag):
        self.canvas.create_line(x0,y0,x1,y1,tags=tag+"_edge")

    def deleteAll(self):
        self.canvas.delete("all")

    def getTag(self,event):
        tag = self.canvas.gettags(self.canvas.find_closest(event.x, event.y))
        tagStr = ""
        for word in tag:
            if word != "current":
                tagStr += " " + word

        return tagStr.strip()


    def clickOnObject(self,event):
        tag = self.getTag(event)
        tkMessageBox.showinfo("Node information", tag)

    def on_token_press(self, event):
        '''Begining drag of an object'''
        # record the item and its location
        self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def on_token_release(self, event):
        '''End drag of an object'''
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0
        #Update our network
        self.animator.updateSystem(10,self,0)



    def on_token_motion(self, event):
        '''Handle dragging of an object'''
        # compute how much the mouse has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        # move the object the appropriate amount
        self.canvas.move(self._drag_data["item"], delta_x, delta_y)
        #update the network position
        node = self.network.nodes[self.getTag(event)]

        node.pos.x += delta_x
        node.pos.y += delta_y

        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def addAnimator(self,animator):
        self.animator = animator


if __name__ == "__main__":
    width = 600
    height= 600
    root = VisualizerFrame(width, height)
    root.mainloop()