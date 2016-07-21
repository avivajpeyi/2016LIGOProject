
Folder = "backgroundAnalysis300July14"      # the folder in which the run was started
numList = [8,16,32,64]                      # the list of durations


import h5py
import numpy as np
from scipy import sparse as sp
import os
import fnmatch
FILE_NAME = 1

def coherentData(BASE_DIR):
    print(Number+ " file for coh")

    fileName = "coh_Bayes_" + Number + ".txt"
    # File to output coherent data in
    coherent_output_file = open(fileName, 'w')
    coherent_output = {}    # string that will contain the output


    # Open the folder in the set dir, and load the names of the file names
    coherent_DIR = BASE_DIR +'/coherence_test/'
    coherent_files = os.listdir( coherent_DIR )

    # Getting the File Names in the coherent_DIR
    file_list = []
    for (dirpath, dirnames, filenames) in os.walk(coherent_DIR):
        for f in filenames:
            if 'coherence_test_H1L1_' in str(f):
                e = os.path.join(str(dirpath), str(f))
                file_list.append(e)

    # extracting the needed files and sorting them
    unsorted_files = []
    sorted_files = []
    for f in file_list:
        # extracting the number from the file name
        dashIndex = f.index("-")
        fnum = f[dashIndex+1:]
        dotIndex = fnum.index(".")
        fnum = fnum[:dotIndex]
        # the number of the file, and then the name
        unsorted_files.append([fnum,f])
    sorted_files= sorted(unsorted_files,key=lambda x: x[0])

    # Opening each file in order, storing GPS time and BayesFactor in output file
    for f in sorted_files:
        txtfile = open(f[FILE_NAME], 'r')
        coherent_output[f[FILE_NAME]] = []
        for line in txtfile:

            # getting the GPS time from file name
            GPStime = f[FILE_NAME]
            GPStime = GPStime[len(coherent_DIR+"coherence_test_H1L1_"):]
            dashIndex = GPStime.index("-")
            GPStime = GPStime[:dashIndex]

            line = line.strip('\n')
            coherent_output_file.write(line + '\t' + GPStime + '\n')
        txtfile.close()

    coherent_output_file.close()
#------------------------------------------------------------------------


def incoherentData(BASE_DIR):
    print(Number+ " file for incoh")

    fileName = "incoh_Bayes_" + Number + ".txt"

    # File to output coherent data in
    incoherent_output_file = open(fileName, 'w')
    incoherent_output = {}    # string that will contain the output

    # Open the folder in the set dir, and load the names of the file names
    incoherent_DIR = BASE_DIR +'/posterior_samples/'

    # get the list of the HDF5 files with the Bayes Factor
    file_list   = []
    for root, dirnames, filenames in os.walk(incoherent_DIR):
     for filename in fnmatch.filter(filenames, 'posterior_H1L1*.hdf5'):
         file_list.append(os.path.join(root, filename))


    # extracting the needed files and sorting them
    unsorted_files = []
    sorted_files = []
    for f in file_list:
        # extracting the number from the file name
        dashIndex = f.index("-")
        fnum = f[dashIndex+1:]
        dotIndex = fnum.index(".")
        fnum = fnum[:dotIndex]
        # the number of the file, and then the name
        unsorted_files.append([fnum,f])
    sorted_files= sorted(unsorted_files,key=lambda x: x[0])

    # Opening each file in order, storing GPS time and BayesFactor in output file

    for hdfFile in sorted_files:

        the_file = h5py.File(hdfFile[FILE_NAME],"r")
        bayesFactor = the_file["/lalinference/lalinference_nest/"].attrs.get('log_bayes_factor')


        GPStime = hdfFile[FILE_NAME]
        GPStime = GPStime[len(incoherent_DIR+"posterior_H1L1_"):]
        dashIndex = GPStime.index("-")
        GPStime = GPStime[:dashIndex]



        outputStr = str(bayesFactor) + '\t' + GPStime + '\n'
        incoherent_output_file.write(str(bayesFactor) + '\t' + GPStime + '\n')

        the_file.close()

    incoherent_output_file.close()
#------------------------------------------------------------------------

# iterating through the list of durations
for num in numList:
    Number = str(num)
    print ("Processing files for duration " + Number + "s...")
    BASE_DIR ="/home/avi.vajpeyi/" + Folder + "/lalinferencenest/IMRPhenomPv2pseudoFourPN/"+Number+'s'
    incoherentData(BASE_DIR)
    coherentData(BASE_DIR)
