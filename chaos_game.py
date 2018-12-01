import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point
import numpy as np
from numpy.random import choice
import random
import math

#MODIFY THESE CONSTANTS!
REGULAR = True                      #Equal sides, equal angle, equal weightss; if not desired, enter vertices manually in main()
N_SIDES = 3                         #Number of sides of the polygon
RADIUS = 1                          #Radius of the polygon
CENTER = (0,0)                      #Position of the center
START_ANGLE = math.pi/2             #pi/2 initial rotation makes top point centered, rather than right point

NO_REPEAT = False                    #The previous vertex cannot be chosen the next time
FACTOR = 0.5                        #Fraction of segment to travel
RESOLUTION = 10**5                  #Number of dots
DOT_SCALE = 10**4                   #Reference dot size

RANDOM_VERTEX_COLORS = True         #Evenly picked colors from a colormap; black if false
RANDOM_CMAP = 'viridis'             #Space to sample random colors from
POLY_COLOR = 'gray'                 #Personal preference
POLY_ALPHA = 0.1                    #Transparency of polygon

class Vertex:
    def __init__(self, p, w, c=(0,0,0)):    #vertex is black by default
        self.position = p
        self.weight = w
        self.color = c

class Poly:
    def __init__(self, verts, bg):
        self.vertices = verts
        self.n = len(verts) #number of vertices
        #Assign random colors
        cmap = plt.get_cmap(RANDOM_CMAP)
        colors = cmap(np.linspace(0, 1, self.n))
        k = 0
        for v in self.vertices:
            v.color = colors[k]
            k+=1

        self.shape = Polygon([v.position for v in self.vertices])   #for checking interior for a random point
        (self.minx, self.miny, self.maxx, self.maxy) = self.shape.bounds    #bounding box
        self.color = bg

    def draw(self, ax):
        vx = [v.position[0] for v in self.vertices]
        vy = [v.position[1] for v in self.vertices]
        ax.fill(vx, vy, color=self.color, alpha=POLY_ALPHA, zorder=-1)  #background polygon
        ax.scatter(vx, vy, s=50, c=[v.color for v in self.vertices], zorder=-1) #vertices

    def pointInside(self):
        while True:
            p = (random.uniform(self.minx, self.maxx), random.uniform(self.miny, self.maxy))    #unifrom random point in bounding box
            if self.shape.contains(Point(p)):   #only accept point if in bounding box
                return p

    def pickVert(self):
        choosenVert = choice(range(self.n), p=[v.weight for v in self.vertices])   #choose 1 vertex using weights
        return self.vertices[choosenVert]

class Dots:
    def __init__(self, p):
        self.poly = p
        self.dots = [self.poly.pointInside()]   #start with random point on interior of polygon
        self.dcolor = [(0,0,0)] #stores color of dot based on which vertex it formed a midpoint with, black for initial point
        self.prevVert = None    #Vertex chosen in pervious iteration

    def midpoint(self, pt1, pt2):
        return (FACTOR * (pt1[0] + pt2[0]), FACTOR * (pt1[1] + pt2[1]))

    def addDot(self, count, noRepeat):
        current = self.dots[count]
        nextVert = self.poly.pickVert()
        if (noRepeat):
            while(nextVert == self.prevVert):        #repick vert if same as previously chosen one
                nextVert = self.poly.pickVert()
        self.prevVert = nextVert
        self.dots.append(self.midpoint(current, nextVert.position))
        self.dcolor.append(nextVert.color)

    def draw(self, ax,fig, resolution):
        for i in range(resolution):
            self.addDot(i, NO_REPEAT)
        dx = [d[0] for d in self.dots]
        dy = [d[1] for d in self.dots]
        ax.scatter(dx, dy, marker='.', s=DOT_SCALE/resolution, c=self.dcolor, zorder=0) #dots
        
        
def main():
    v = []  #vertices of polygon
    if (REGULAR):
        angle = START_ANGLE
        angle_increment = 2*math.pi / N_SIDES
        for i in range(N_SIDES):
            x = CENTER[0] + RADIUS * math.cos(angle)    #basic trig
            y = CENTER[1] + RADIUS * math.sin(angle)
            v.append(Vertex((x, y), 1.0/N_SIDES))
            angle += angle_increment
    else:
        v = [Vertex((0,0), 1.0/2.0), Vertex((1,0), 1.0/4.0), Vertex((0,1), 1.0/4.0)]  #Set-up your custom points here

    p = Poly(v, POLY_COLOR)
    d = Dots(p)

    fig, ax = plt.subplots(figsize=(9,9))
    fig.canvas.set_window_title("Chaos Game")
    fig.suptitle("n-gon Chaos Game", size=16, ha='center')
    plt.gca().set_aspect('equal')

    p.draw(ax)
    d.draw(ax, fig, RESOLUTION)
    plt.show()

main()