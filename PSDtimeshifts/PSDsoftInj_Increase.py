import numpy as np
import os
import sys
import fileinput
from tempfile import mkstemp
from shutil import move
from os import remove, close





fileToSearch = '/home/avi.vajpeyi/softwareInjections/lalinferencenest/IMRPhenomPv2pseudoFourPN/8s/lalinference_1127623539.847713-1127653939.847713.dag' #

def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    with open(abs_path,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    close(fh)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)
####################################

def removeHashLine(fileToSearch):
    f = open(fileToSearch,"r")
    lines = f.readlines()
    f.close()
    f = open(fileToSearch, 'w')
    f.writelines([item for item in lines if '##' not in item])
    f.close()
####################################



def increasingPSDstartTime(dagToEdit):
    # load in the lines that we need to edit
    f = open(dagToEdit,"r")
    lines = f.readlines()
    f.close()

    # remove all the comments to make life easier
    removeHashLine(dagToEdit)

    # iterating through all the lines
    for line in lines:

        # if the line is a VARs line, adjust the PSD start
        if "VARS " and " macrotrigtime="  in line:


            #---> break line up into its components
            lineBreakup = line.split('"')

            #---> find the trig time in the VARstring (macrotrigtime="1127624139")
            trigIndex = lineBreakup.index(' macrotrigtime=') + 1
            trigValue = lineBreakup[trigIndex]

            #---> find the PSD start
            PSDstartIndex = lineBreakup.index(' macropsdstart=') + 1
            currentPSDval = lineBreakup[PSDstartIndex]

            #---> generate a new VAR string with new PSD Start = Trig + 10
            lineWithoutPSDstart = line.split(currentPSDval)
            newPSDstart = str(float(trigValue) + 10.0)
            newVARstring = lineWithoutPSDstart[0] + newPSDstart + lineWithoutPSDstart[1]
            print("old:")
            print(line)
            print("New:")
            print(newVARstring)
            print("\n\n")
            #---> Replace the new VARs with the old VARs
            replace(dagToEdit, line, newVARstring)

####################################

increasingPSDstartTime(fileToSearch)
