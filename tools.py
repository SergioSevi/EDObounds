import numpy as np
import os
Lensinglist=['EROS-2','OGLE-IV','Subaru-HSC']

import os

#Function that gets all files in a bound. Used to get the closest bound applying to a given radius, in the case it is not present.
def list_files_in_directory(directory):
    txt_files_list = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                txt_files_list.append(os.path.join(root, file))

    return txt_files_list

#Function necessary to find the minima of all lensing bounds
def min_function(x,all_points):
    min_value = np.inf
    for x_list, y_list in all_points:
        y_value = np.interp(x, x_list, y_list)
        min_value = min(min_value, y_value)
    return min_value

def load_bound(boundID,shape,radius):
    all_points=[]
    min_x=np.inf
    max_x=-np.inf
    #If lensing, then run the code below to each bound and take the minimum
    if boundID == "Lensing":
        for i in range(len(Lensinglist)):
            try:
                m1, f1 = np.loadtxt('bounds/' + Lensinglist[i] + '/' + shape + '/r' + str(radius) +'.txt', unpack=True)
            except:
                try:
                    directory_path = 'bounds/' + Lensinglist[i] + '/' + shape 
                    files = list_files_in_directory(directory_path)
                    rinfiles = [max(radius,int(x[x.index("/r")+2:x.index(".")])) for x in files]
                    rinfiles=min([x for x in rinfiles if x != radius])
                    m1, f1 = np.loadtxt('bounds/' + Lensinglist[i] + '/' + shape + '/r' + str(rinfiles) +'.txt', unpack=True)
                except:
                    m1, f1= [[11+i,10+i],[11+i,9+i]]
            all_points.append((m1, f1))
            min_x=min(min(m1),min_x)
            max_x=max(max(m1),max_x)
        m1 = np.linspace(np.log10(min_x), np.log10(max_x), 1000)
        m=[10**x for x in m1]
        f = [min_function(10**x,all_points) for x in m1]
    else:
            try:
                m, f = np.loadtxt('bounds/' + boundID + '/' + shape + '/r' + str(radius) +'.txt', unpack=True)
            except:
                try:
                    #If specific bounds for a radius R do not exist, then take those for the next biggest radius.
                    directory_path = 'bounds/' + boundID + '/' + shape 
                    files = list_files_in_directory(directory_path)
                    rinfiles = [max(radius,int(x[x.index("/r")+2:x.index(".")])) for x in files]
                    rinfiles=min([x for x in rinfiles if x != radius])
                    m, f = np.loadtxt('bounds/' + boundID + '/' + shape + '/r' + str(rinfiles) +'.txt', unpack=True)
                except:
                    m, f= [[11,10],[11,9]]

    return m, f