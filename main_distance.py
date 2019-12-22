# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 18:52:32 2019

@author: yzz
"""

import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from celluloid import Camera
from functions import vehicle, insert, update, distance, distance_path

# read nodes from file
nodes = pd.read_csv('input/demands.csv', index_col = 'node')

# create a dictionary to store Origin-Destination pairs
# the key of the dict is the time the OD demand shows up
OD_time = dict()
number_demand = int((len(nodes.index) - 1) / 2)
for i in range(1, number_demand + 1):
    key = float(nodes['time'][i])
    OD_time[key] = (nodes.index[i], nodes.index[i + number_demand]) # if unserved

# create a list of drop-off nodes for future reference
df_drop_off = nodes.loc[nodes['label'] == 2]
drop_off = list(df_drop_off.index)

# -------
# Define parameters

customer_cap = 2 # define maximum capacity of each vehicle
n_v = 2 # define fleet size

# initiate vehicle fleet
vehs = list()
for v in range(n_v):
    vehs.append(vehicle())
    
total_distance = 0 # initialize total travel length

t = 0 # initialize time
t_max = 26 # maximum time simulated

speed = 1 # speed of the vehicle
dt = 1 # time step

OrDes = [0] # define OD pairs that have shown up
demand_list = list() # define initial demand

# initiate plot for animation
fig, ax = plt.subplots(figsize = (7, 5))
camera = Camera(fig)

while t < t_max:
    # read-in Origin-Destination pair
    new_demand = True
    try:
        OrDe_new = OD_time[t]
        ODnodes = list(OrDe_new)
        for ODnode in ODnodes:
            OrDes.append(ODnode)
    except:
        new_demand = False
    
    if new_demand:
        demand_list.append(OrDe_new)
        
    # create a list of potential candidate vehicles to serve this OrDe
    candidate_vehs = list()
    
    # try to assign unassigned OD pairs in demand_list
    for OrDe in demand_list:
    # loop over all vehicles to find shortest increase of total distance
        for veh in vehs:
            # if this vehicle still has extra capacity, add an OD pair to it
            if veh.customer < customer_cap:
                # if this vehicle has a path already, insert a new path
                if len(veh.path) > 0:

                    # find all possible paths through insertion
                    paths = insert(veh.path, OrDe)
                    #print('paths: ', paths)
                    dist_min = np.inf
                    path_sel = paths[0]

                    # find the path with minimum length
                    for path in paths:

                        dist0 = distance_path(veh.x, veh.y, path, nodes)
                        # record minimum length and the corresponding path
                        if dist0 < dist_min:
                            dist_min = dist0
                            dist_add = dist_min - distance_path(veh.x, veh.y, veh.path, nodes)
                            path_sel = path

                # if this vehicle does not has a path, create a new path for it  
                else:
                    O = OrDe[0]
                    D = OrDe[1]
                    dist_min = distance(veh.x, veh.y, nodes['x'][O], nodes['y'][O])
                    dist_min += distance(nodes['x'][O], nodes['y'][O], nodes['x'][D], nodes['y'][D])
                    dist_add = dist_min
                    path_sel = list(OrDe)

                # record candidate vehicle id, min distance added, and the corresponding path        
                candidate_vehs.append([vehs.index(veh), dist_add, path_sel])

            #print('veh_sel: ', vehs.index(veh), '. dist_add: ', dist_add, '. path_sel: ', path_sel)
        
        # If there is any candidate vehicle being selected
        if len(candidate_vehs) > 0:
            # compare candidate vehicles, select the one with minimum dist_add
            df_cv = pd.DataFrame(candidate_vehs, columns = ['id', 'dist_add', 'path'])
            
            total_distance += df_cv['dist_add'].min() # add minimum increase to total distance
            index = df_cv[['dist_add']].idxmin() # get index of the corresponding vehicle

            veh_index = int(df_cv['id'][index])
            path_sel = list(df_cv['path'][index])[0] # identify seleted path
            vehs[veh_index].update_path(list(path_sel)) # update path of this vehicle
            vehs[veh_index].add_customer(1) # add 1 customer to this vehicle
            
            demand_list.remove(OrDe) # remove this OD pair from demand list as it has been assigned

    # print time
    if new_demand:
        print('--- t = ', t, ': ', ' demand ', OrDe_new)
    else:
        print('--- t = ', t, ': ')
    ax.text(-5, 4, 't = ' + str(t))
    
    # plot all showed OD pairs      
    df_OrDes = nodes[nodes.index.isin(OrDes)]
    x = list(df_OrDes['x'])
    y = list(df_OrDes['y'])

    ax.scatter(x, y, marker = 'o', color = 'blue')    
    for i, label in enumerate(list(df_OrDes.index)):
        ax.annotate(label, (x[i], y[i]), xytext = (x[i] - 0.2, y[i] + 0.08))
        
    # print and plot all vehicles   
    for i in range(len(vehs)):
        print('veh ', i, ':')
        print('   path: ', vehs[i].path)
        print('   load: ', vehs[i].customer)
        print('   position: [', round(vehs[i].x, 2) , ',',round(vehs[i].y, 2), ']')
        
        colors = ['#cc5d2d', '#1b8a19', '#8a7019', '#19198a', '#8a1979']
        ax.plot(vehs[i].x, vehs[i].y, marker = '*', color = colors[i])
        label = 'veh_' + str(i) + ' (load: ' + str(vehs[i].customer) + ')'
        ax.annotate(label, (vehs[i].x, vehs[i].y), xytext = (vehs[i].x + 0.08, vehs[i].y + 0.08), color = colors[i])
        xp = [vehs[i].x]
        yp = [vehs[i].y]
        for node in vehs[i].path:
            xp.append(nodes['x'][node])
            yp.append(nodes['y'][node])
        for ixp in range(len(xp) - 1):
            dxp = xp[ixp + 1] - xp[ixp]
            dyp = yp[ixp + 1] - yp[ixp]
            ax.arrow(xp[ixp], yp[ixp], dxp, dyp, head_width = 0.25, color = colors[i], length_includes_head = True)
        ax.set_xlim(-6, 6)
        ax.set_ylim(-4, 5)
    
    print('total_distance: ', round(total_distance,2))
    
    plt.show()
    camera.snap()
    
    # Update time
    t += dt
    
    # update entire fleet
    vehs = update(nodes, vehs, speed, dt, drop_off)
    # remove visited nodes
    for veh in vehs:
        for visited_node in veh.visited:
            if visited_node in OrDes:
                OrDes.remove(visited_node)
                            
animation = camera.animate()
animation.save('vrp_min_distance_origin.gif', writer = 'imagemagick')