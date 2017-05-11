import sys
from MyIO import ReadWriteXslx

sys.setrecursionlimit(200000)

class Animator():
    def __init__(self, settingsDict, *args, **kwargs):
        # Set all the variables
        self.nodeList, self.edgesList = ReadWriteXslx.readNetworkData(settingsDict["path"])
        self.timestep = settingsDict["t"]
        self.radius = settingsDict["radius"]
        self.network = settingsDict["network"]
        self.statusVar = settingsDict["statusVar"]

        #Add missing nodes and put things in a useful format
        self.createMissingNodes()
        self.nodeList = list(set(self.nodeList))

        # Initialize our system
        self.network.initialize(self.nodeList, self.edgesList)

    def createItems(self,visualizer):
        for i in range(len(self.network.nodes.keys())):
            nodeTag = self.network.nodes.keys()[i]
            nodePosX = self.network.nodes.values()[i].pos.x
            nodePosY = self.network.nodes.values()[i].pos.y
            visualizer.createNode(nodePosX,nodePosY,self.radius,fill="blue",tag = nodeTag)

        for edge in self.network.edges:
            x0 = self.network.nodes[edge[0]].pos.x
            y0 = self.network.nodes[edge[0]].pos.y
            x1 = self.network.nodes[edge[1]].pos.x
            y1 = self.network.nodes[edge[1]].pos.y
            visualizer.createEdge(x0,y0,x1,y1,edge[0])


    def createMissingNodes(self):
        for edge in self.edgesList:
            if edge[0] not in self.nodeList:
                self.nodeList.append(edge[0])
            if edge[1] not in self.nodeList:
                self.nodeList.append(edge[1])

    def updateSystem(self,iter,visualizer,index):
        if index < iter:
            self.statusVar.set(str(index) + " of " + str(iter) + " iterations")
            #Update
            self.updateNetwork()
            self.updateVisualizer(visualizer)
            visualizer.after(10, self.updateSystem(iter,visualizer,index + 1))
        else:
            self.statusVar.set("Done")

    def updateNetwork(self):
        self.network.updateParticles(self.timestep)

    def updateVisualizer(self,visualizer):
        visualizer.deleteAll()
        self.createItems(visualizer)
        visualizer.update()


def run(settingsDict):
    animator = Animator(settingsDict)

    #Run our system
    index = 0
    visualizer = settingsDict["visualizer"]
    print "before added"
    visualizer.addAnimator(animator)
    iter = settingsDict["iter"]
    animator.createItems(visualizer)
    animator.updateSystem(iter,visualizer,index)




