#!/usr/bin/env python
#-*-coding:utf-8-*-
#This program creates a 3D vector plot of magnetic field directions obtained by the Sense HAT.
#Created by Peter Apps

import csv
import matplotlib
matplotlib.use("Agg") #Added to plot graphs without running X server.
import matplotlib.pyplot as plt
#from matplotlib.ticker import FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from sense_hat import SenseHat
import time

#Define list needed for the plot.
i = []
x = [] 
y = [] 
z = []
count = 0
snooze = .2 #Time in seconds for the time.sleep().
continueLoop = True

def saveData():
    continueLoop = False
    file = open("/home/pi/magfield.csv", "a") #Opens file to save data.
    writer = csv.writer(file, delimiter = ",")
    data = [i, x, y, z]
    writer.writerows(data) #Writes data on the csv file.
   
    if len(x) == len(y) and len(y) == len(z):        
        print("All Lengths Match, Constructing Graph")
        makeGraph()
    else:
        print("Length's Don't Match, can't create graph!")    
   
def makeGraph():
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    #setup grid for plot (should autoscale based on the largest values in x/y/z)
    a,b,c = np.meshgrid(np.arange(-max(x),max(x), 2*max(x)/len(x)),
                        np.arange(-max(y),max(y), 2*max(y)/len(y)),
                        np.arange(-max(z),max(z), 2*max(z)/len(z)))
    
##    ax.xaxis.set_major_formatter(FormatStrFormatter("%.2f")) #Formats the data in the axis with 2 decimal places.
##    ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))
##    ax.zaxis.set_major_formatter(FormatStrFormatter("%.2f"))
    ax.set_xlabel(u"x (\u00B0)") #x axis label.
    ax.set_ylabel(u"y (\u00B0)") #y axis label.
    ax.set_zlabel(u"z (\u00B0)") #z axis label.

    #Plot the vectors on the graph
    ax.quiver3D(a, b, c, x, y, z, length=0.075)

    plt.show()
    plt.savefig("/home/pi/magField.png",dpi='figure', format='png') #Saves the plot with the optimal size.
    #plt.clf() #Clears the plot, in order to get a tidy plot.
    print("Graph Saved")

while continueLoop:
    sense = SenseHat()
    rawCompass = sense.get_compass_raw()
    xcomponent = round(rawCompass["x"], 2)
    ycomponent = round(rawCompass["y"], 2)
    zcomponent = round(rawCompass["z"], 2)
    count += 1
    
    i.append(count) #Updates list for the plot.
    x.append(xcomponent)
    y.append(ycomponent)
    z.append(zcomponent)

    if len(sense.stick.get_events()): #if the joystick is moved, end the loop
        continueLoop = False
    time.sleep(snooze) #Code is each x seconds, defined as snooze before the while loop.

saveData()
