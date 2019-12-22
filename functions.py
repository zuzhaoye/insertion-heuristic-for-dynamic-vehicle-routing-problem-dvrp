# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 18:55:06 2019

@author: yzz
"""

import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from copy import deepcopy

# Define vehicle
class vehicle():
    def __init__(self):
        self.x = 0  # x coordinate
        self.y = 0  # y coordinate
        self.customer = 0 # number of customers
        self.path = list() # path assigned to this vehicle
        self.visited = list()
        
    def update_pos(self, x, y):
        self.x = x
        self.y = y
        
    def add_customer(self, customer):
        self.customer += customer
        
    def update_path(self, path):
        self.path = path
        
    def update_visited(self, node):
        self.visited.append(node)

#Define a function that inserts a new OD pair into an existing path
#- Pick-up is always ahead of drop-off
#- Return all possible paths       
def insert(path, new_OD):
    paths = list()
    O = new_OD[0]
    D = new_OD[1]
    for i in range(len(path) + 1):
        path1 = deepcopy(path)
        path1.insert(i, O)
        k = path1.index(O) + 1
        for j in range(k, len(path1) + 1):
            path2 = path1.copy()
            path2.insert(j, D)
            paths.append(path2)
            
    return paths

# Define a function to update vehicle's position, load, and path
def update(nodes, vehs, speed, dt, drop_off):

    d = speed * dt
    vehs_new = list()
    
    for veh in vehs:
        
        if len(veh.path) > 0:
            
            # obtain a list of unvisited nodes
            visited = veh.visited
            unvisited = deepcopy(veh.path)
            for node in veh.path:
                if node in visited:
                    unvisited.remove(node)
     
            # calculate the distance of vehicle to all unvisited nodes      
            dist = list()
            n1 = unvisited[0]
            x1 = nodes['x'][n1]
            y1 = nodes['y'][n1]
            dist_1_0 = distance(veh.x, veh.y, x1, y1)
                        
            if d < dist_1_0: # if not over reach, calcultate the distance based on (veh -> n1)
                sign = 1
                if x1 < veh.x:
                    sign = -1
                direct = (veh.y - y1) / (veh.x - x1)
                dx = (1 / (1 + direct ** 2)) ** 0.5 * d
                dy = direct * dx
                veh.x = veh.x + sign * dx
                veh.y = veh.y + sign * dy
            
            else: # if over reach, calculate distance based on (n1 -> n2)
                # if there is still nodes next
                if len(unvisited) > 1:
                    delta_d = d - dist_1_0
                    n2 = unvisited[1]
                    x2 = nodes['x'][n2]
                    y2 = nodes['y'][n2]
                    
                    sign = 1
                    if x2 < x1:
                        sign = -1
                    direct = (y2 - y1) / (x2 - x1)
                    dx = (1 / (1 + direct ** 2)) ** 0.5 * delta_d
                    dy = direct * dx
                    veh.x = x1 + sign * dx
                    veh.y = y1 + sign * dy
                
                # all the nodes are visited, the vehicle shall stay on the final position until further notice
                else:
                    veh.x = x1
                    veh.y = y1
                                    
                veh.update_visited(n1) # add n1 to visited node
                veh.path.remove(n1) # remove n1 from the path
                
                # if n1 is a drop-off node
                if n1 in drop_off:
                    veh.add_customer(-1) # reduce 1 customer
                
            vehs_new.append(veh)
            
        else:
            vehs_new.append(veh)
            
    return vehs_new

# Auxilary functions to calculate:
    
# 1. point-point distance
def distance(x1, y1, x2, y2):
    dist = (x1 - x2) ** 2 + (y1 - y2) ** 2
    dist = dist ** 0.5
    return dist

# 2. path total length
def distance_path(vehx, vehy, path, nodes):
    n1 = path[0]
    x1 = nodes['x'][n1]
    y1 = nodes['y'][n1]
    dist0 = distance(vehx, vehy, x1, y1)
    
    for i in range(len(path) - 1):
        n1 = path[i]
        n2 = path[i + 1]
        x1 = nodes['x'][n1]
        y1 = nodes['y'][n1]
        x2 = nodes['x'][n2]
        y2 = nodes['y'][n2]
        dist0 += distance(x1, y1, x2, y2)
        
    return dist0

# total waiting time of a path
def waiting_time(vehx, vehy, path, nodes, drop_off, speed):
    
    # find out drop-off nodes in the path
    path_dropoff = list()
    for node in path:
        if node in drop_off:
            path_dropoff.append(node)
    
    # calculate waiting time for each dropoff
    #waiting time = veh -> dropoff1 + veh -> dropoff2 + ... + veh -> dropoffn  
    waiting_time = 0
    for node in path_dropoff:
        index_dropoff = path.index(node)        
        path_temp = path[:index_dropoff + 1]
        waiting_time += distance_path(vehx, vehy, path_temp, nodes) / speed
                
    return waiting_time