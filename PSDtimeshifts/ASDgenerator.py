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

            file_list.append(os.path.join(subdir, file))


# We need to make new ASD files for each PSD file we have
for f in file_list:
    print (f)
    # takes the data for the Freq and PSD
    dataMatrix = np.loadtxt(f)

    #Transposing the Data Matrix and rooting the PSD
    dataMatrix = dataMatrix.T
    dataMatrix[1]=np.sqrt(dataMatrix[1])
    dataMatrix = dataMatrix.T

    # Creating a new file to store ASDarray in
    index = f.index("PSD.dat")# idex where PSD.dat begins
    newFileName =f[:index]# Getting the subtring of everything before PSD.dat
    newFileName = newFileName+"ASD.dat"
    np.savetxt(newFileName, ASDarray)
