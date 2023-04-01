# Matt Daves
# CSC 445 Graph Assignment 3
# Sources:
#    https://matplotlib.org/stable/index.html
#    Install cmd: python -m pip install -U matplotlib

import matplotlib.pyplot as plt
import tkinter.filedialog
from math import dist
from collections import defaultdict
from matplotlib.artist import Artist
from matplotlib.lines import Line2D
from matplotlib.collections import PathCollection
import numpy as np

# Class for Node object
class point:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
     
pointFrom = None
pointTo = None

def main():
    nodes = 0
    points = []
    edges = []
    x = [] 
    y = [] 
    g = []
    p = []
    e = []
    g.append(p)
    g.append(e)
    myColor = "grey" 
    path = tkinter.filedialog.askopenfilename()
    
    # method to handle Node's click event
    def onPick(event):
        result = defaultdict(dict)
        for edge in g[1]:
            v1, v2 = edge[0]
            result[v1][v2] = edge[1]
            result[v2][v1] = edge[1]
        global pointFrom
        global pointTo
        global id1
        global id2
        global pFrom
        global pTo
        if event.mouseevent.button == 1:
            if pointFrom == None:
                pointFrom = event.artist
                props = {"color": "green"}
                Artist.update(pointFrom, props)
            else:
                props = {"color": "grey"}
                Artist.update(pointFrom, props)
                newPoint = event.artist
                props = {"color": "green"}
                Artist.update(newPoint, props)
                pointFrom = newPoint

            line = event.artist
            id1 = line.get_offsets()
            id1 = np.ma.getdata(id1[0])
            pFrom = matchOffset(id1)
            try:
                dijkstras(result,pFrom, pTo)
            except:
                UnboundLocalError

        if event.mouseevent.button == 3:
            if pointTo == None:
                pointTo = event.artist
                props = {"color": "blue"}
                Artist.update(pointTo, props)
            else:
                props = {"color": "grey"}
                Artist.update(pointTo, props)
                newPointTo = event.artist
                props = {"color": "blue"}
                Artist.update(newPointTo, props)
                pointTo = newPointTo

            line = event.artist
            id2 = line.get_offsets()
            id2 = np.ma.getdata(id2[0])
            pTo = matchOffset(id2)
            try:
                dijkstras(result,pFrom, pTo) 
            except: 
                NameError
        plt.show()
        return
    # helper method to match an artist object's location (offset) with the name of the corrsponding point's name
    def matchOffset(offset):
        for point in points:
            if point.x == offset[0] and point.y == offset[1]:
                return point.name
    # helper method
    def getPathEdges(edges):
        pathEdges = []
        for i in range(len(edges)-1):
            pathEdges.append(edges[i] + "-" + edges[i+1])
            pathEdges.append(edges[i+1] + "-" + edges[i])
        return pathEdges             
    # helper method to redraw edges and points when diskstras is recalculated
    def redraw(nodes, pathEdges):
        tempPoints = []
        nonPathPoints = []
        props = {"color": "green"}
        props2 = {"color": "grey"}
        for node in nodes[1:-1]:
            tempPoints.append(points[int(node)])

        for p in points:
            if p.name not in nodes:
                nonPathPoints.append(p)
         
        plotstemp = plot.get_children()
        
        for p in plotstemp:
            if isinstance(p, Line2D):
                if p.get_label() not in pathEdges:
                    Artist.update(p,{"color":"black"})

                for edge in pathEdges:
                    if p.get_label() == edge:
                        Artist.update(p,props)
                        
            elif isinstance(p,PathCollection):
                for po in nonPathPoints:
                    tempPLoc = p.get_offsets()
                    pLoc = np.ma.getdata(tempPLoc[0])
                    
                    if po.x == pLoc[0] and po.y == pLoc[1]:  
                        Artist.update(p,props2)
                        
                for point in tempPoints:
                    tempPLoc = p.get_offsets()
                    pLoc = np.ma.getdata(tempPLoc[0])
                    
                    if point.x == pLoc[0] and point.y == pLoc[1]:                       
                        Artist.update(p, props)
    # helper method to calculate distance between points
    def distance(point1, point2):
        p1 = points[int(point1)]
        p2 = points[int(point2)]
        node1 = [p1.x, p1.y]
        node2 = [p2.x, p2.y]
        return dist(node1, node2)
    # helper method used for drawing our edges 
    def drawLine(nodeFrom, nodeTo, lineColor):
        p1 = points[nodeFrom]
        p2 = points[nodeTo]
        x = [p1.x, p2.x]
        y = [p1.y, p2.y]
        return plt.plot(x, y, color = lineColor, zorder = 0, label=str(nodeFrom)+"-"+str(nodeTo),linewidth = 2.5)
    # method to calculate shortest path between two nodes      
    def dijkstras(graph, start, end):
        if graph.get(start) == None or graph.get(end) == None:
            plt.title("Path is not reachable")
            return
        shortestDistance = {}
        trackPredecessor = {}
        unseenNodes = graph
        infinity = float("inf")
        currentPath = [] 
        
        for node in unseenNodes:
            shortestDistance[node] = infinity
        shortestDistance[start] = 0
        
        while unseenNodes:
            minDistanceNode = None
            
            for node in unseenNodes:
                if minDistanceNode is None:
                    minDistanceNode = node
                elif shortestDistance[node] < shortestDistance[minDistanceNode]:
                    minDistanceNode = node
                    
            pathOptions = graph[minDistanceNode].items()
            
            for childNode, weight in pathOptions:
                if weight + shortestDistance[minDistanceNode] < shortestDistance[childNode]:
                    shortestDistance[childNode] = weight + shortestDistance[minDistanceNode]
                    trackPredecessor[childNode] = minDistanceNode
                    
            unseenNodes.pop(minDistanceNode)
            
        currentNode = end
        
        while currentNode != start:
            try:
                currentPath.insert(0, currentNode)
                currentNode = trackPredecessor[currentNode]
            except KeyError:
                plt.title("path is not reachable")
                break
            
        currentPath.insert(0,start)
        
        if shortestDistance[end] != infinity:
            plt.title("Shortest Distance is " +  "{:.2f}".format(shortestDistance[end]) +
                  "\n" + "Optimal Path is " + str(currentPath))
            
        redraw(currentPath,getPathEdges(currentPath))
         
    # code to read input from file and store information to create points and edges
    try:
        with open(path) as f:
            plots = []
            f = f.readlines()
            index = 0
            nodeNum = 0
            needEdgeNum = True
            fig, plot = plt.subplots(num="Matt Daves Graph Assignment")
            for line in f:
                if index == 0:
                    nodes = int(line.strip())
                    index += 1 
                elif index <= nodes:
                        row = line.strip().replace(" ", "").split(",")    
                        points.append(point(float(row[0]), float(row[1]),str(nodeNum)))
                        x.append(float(row[0]))
                        y.append(float(row[1]))
                        plots.append(plot.scatter(float(row[0]),float(row[1]), s = 500, picker = True, color = myColor))
                        plot.annotate(nodeNum,(float(row[0])-.2,float(row[1])-.5),fontsize=15)
                        p.append(index-1)
                        index += 1
                        nodeNum += 1      
                else:
                    line = line.strip()
                    if line == "":
                        continue
                    else:
                        if needEdgeNum:
                            needEdgeNum = False
                        else:
                            row = line.split()
                            var = distance(row[0], row[1])
                            e.append(({row[0], row[1]}, var))
                            edges.append(drawLine(int(row[0]), int(row[1]), "black"))
    except FileNotFoundError:
        return
    
    # code to configure plot
    enumerate(points)
    plt.ylim(min(y) - 5, max(y) + 5)
    plt.xlabel('x axis') 
    plt.ylabel('y axis') 
    fig.canvas.callbacks.connect('pick_event', onPick)
    plt.show()
    
if __name__ == "__main__":
    main()