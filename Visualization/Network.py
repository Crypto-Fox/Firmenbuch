import Vector
import random as rd
import Forces


class Node:
    def __init__(self,position=Vector.Vector2D(0,0),name="Placeholder", colour="blue",size=1):
        self.name = name
        self.colour = name
        self.pos = position


class Edge:
    def __init__(self,node1,node2):
        self.node1 = node1
        self.node2 = node2


class Network:
    def __init__(self,size_x,size_y,spring):
        self.nodes = "NA" #dict
        self.edges = "NA" #dict
        self.size_x =size_x
        self.size_y = size_y
        self.spring = spring

    def initialize(self,nodes,edges):
        self.populateNodes(nodes)
        self.populateEdges(edges)
        self.random_dist()


    def random_dist(self):
        for node in self.nodes.values():
            node.pos = Vector.Vector2D(rd.random()*self.size_x,rd.random()*self.size_y)


    def calculateForces(self):
        forces = dict()
        #First loop through our nodes and perform the particle forces
        for i in range(len(self.nodes.keys())):
            node = self.nodes.keys()[i]
            forces[node] = Vector.Vector2D(0,0)
            for j in range(len(self.nodes.keys())):
                if i!=j:
                    forces[node] = Vector.vectorAdd(forces[node],Forces.force_cube_repulsion(self.nodes[node].pos,self.nodes.values()[j].pos))
                    forces[node] = Vector.vectorAdd(forces[node],Forces.force_square_attractive(self.nodes[node].pos,self.nodes.values()[j].pos))


        #Now loop through our edges
        for edge in self.edges:
            node1 = edge[0]
            node2 = edge[1]
            force = Forces.springForce(self.nodes[node1].pos,self.nodes[node2].pos,self.spring)
            forces[node1] = Vector.vectorAdd(forces[node1],force)
            forces[node2] = Vector.vectorAdd(forces[node2], force.invert())

        return forces

    def updateParticles(self,t):
        forces = self.calculateForces()
        for i in range(len(forces.keys())):
            node = forces.keys()[i]
            pos = self.nodes[node].pos
            newPos = Vector.vectorAdd(pos,Vector.scalar_multiply(forces[node],t))
            self.nodes[node].pos = newPos

        #Ensure we remain inside our box
        self.ensureBounding()

        return forces

    def ensureBounding(self):
        for node in self.nodes.values():
            #x
            if node.pos.x > self.size_x-50:
                node.pos.x -= 10
            if node.pos.x < 50:
                node.pos.x +=10
            #y
            if node.pos.y > self.size_y-50:
                node.pos.y -= 10
            if node.pos.y < 50:
                node.pos.y +=10


    #Currently this will be hardcoded upload of particles, but this will change when we have a file IO as well or passing it the nodes
    def populateNodes(self,nodeList):
        self.nodes = dict()
        for node in nodeList:
            self.nodes[node]=Node(name=node.strip())


    def populateEdges(self,edgeList):
        self.edges = edgeList




if __name__ == "__main__":
    nodeList = ["alpha","beta","gamma","delta","epsilon","zeta"]
    edgeList = [("alpha","beta"),("gamma","delta"),("epsilon","zeta"),("zeta","alpha")]
    network = Network(300,300,10)
    network.initialize(nodeList,edgeList,100,0.1)


