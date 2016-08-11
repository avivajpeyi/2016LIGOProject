import numpy as np
import os
import sys
import fileinput
from tempfile import mkstemp
from shutil import move
from os import remove, close


rootdir ='/home/avi.vajpeyi/pycbcBackgroundTriggers/lalinferencenest/IMRPhenomPv2pseudoFourPN/8s/ROQdata/timeshiftedROQfiles/'

file_list   = []
# get the list of timeshifted PSD files
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if 'data-dumpL1-PSD.dat' in str(file):
            print os.path.join(subdir, file)
            file_list.append(os.path.join(subdir, file))


# We need to make new ASD files for each PSD file we have
for f in file_list:
    # takes the data for the Freq and PSD
    dataMatrix = np.loadtxt(f)
    ASDarray = []
    for n in range(len(dataMatrix)):
        # item will store each specific Freq and PSD from the dataMatrix
        item =[]
        item.append(dataMatrix[n][0])
        item.append(np.sqrt(dataMatrix[n][1])) # ASD = SQRT (PSD)
        ASDarray.append(item)

        # Creating a new file to store ASDarray in
        index = f.index("PSD.dat")# idex where PSD.dat begins
        newFileName =f[:index]# Getting the subtring of everything before PSD.dat
        newFileName = newFileName+"ASD.dat"
        np.savetxt(newFileName, ASDarray)
