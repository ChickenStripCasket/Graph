#Matt Daves
#CSC 445 Graph Assignment 2
#Sources:
#   https://matplotlib.org/stable/api/matplotlib_configuration_api.html
#   Install cmd: python -m pip install -U pip
#                python -m pip install -U matplotlib


import matplotlib.pyplot as plt
import tkinter.filedialog

#Class for Node object
class point:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name

def main():
    x = [] 
    y = [] 
    nodes = 0
    points = []
    path = tkinter.filedialog.askopenfilename()
    
    #method used for drawing our edges 
    def drawLine(nodeFrom, nodeTo):
        p1 = points[nodeFrom]
        p2 = points[nodeTo]
        x = [p1.x, p2.x]
        y = [p1.y, p2.y]
        plt.plot(x, y, color = "black", zorder = 0)
    
    #method to handle Node's click event
    def onClick(event):
        ind = event.ind[0]
        node = points[ind]
        plt.title("Coordinates of " + str(node.name) + ":" +
                   "\n    X=" + str(node.x) + "     Y=" + str(node.y),
                   fontsize=15)
        plt.show()
        return
    
    #code to read input from file and store information to create points and edges
    with open(path) as f:
        
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

                    points.append(point(float(row[0]), float(row[1]), "Node " + str(nodeNum)))
                    x.append(float(row[0]))
                    y.append(float(row[1]))
                    plot.annotate(nodeNum,(float(row[0])-.12,float(row[1])-.4),fontsize=12)

                    index += 1
                    nodeNum += 1      
            else:
                line = line.strip()
                if line == "":
                    continue
                else:
                    if needEdgeNum:
                        edgeNum = int(line.strip())
                        needEdgeNum = False
                    else:
                        row = line.split()
                        drawLine(int(row[0]), int(row[1]))
    
    #code to configure plot and add points
    enumerate(points)
    plt.ylim(min(y) + (min(y)*.50), max(y) + (max(y)*.50))
    plot.scatter(x,y, s = 500, picker = True)
    plt.xlabel('x axis') 
    plt.ylabel('y axis') 
    fig.canvas.callbacks.connect('pick_event', onClick)
    plt.show()

if __name__ == "__main__":
    main()

