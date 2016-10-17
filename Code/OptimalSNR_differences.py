
import h5py
import numpy as np
from scipy import sparse as sp
import os
import fnmatch


Folder = 'pycbcBackgroundTriggers'
numList = [8,16,32,64]                      # the list of durations


def Coherent_OptimalSNR(directory, num):

    print("...\n" "\t Processing Coherent Data...\n")
    #output file to write Optimal SNRs into
    OutputFileName = "OptSNR"+num+"H1L1Coh.txt"
    output_file = open(OutputFileName, 'w')
    output_file.write("File \t GPStime \t HCoh"+num+"\t LCoh"+num+'\n')

    #directory = "/home/avi.vajpeyi/pycbcBackgroundTriggers/lalinferencenest/IMRPhenomPv2pseudoFourPN/8s/posterior_samples/"

    hdfList   = []
    # Creates a list of the HDF5 file names that need to be accessed
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, 'posterior_H1L1*.hdf5'):
            hdfList.append(os.path.join(root, filename))
    sizeOfList = len(hdfList)
    count = 0
    # Opens each HDF5 file needed and extracts the GPStime, H and L optimal SNR
    for hdfFile in hdfList:
        the_file = h5py.File(hdfFile,"r")
        L_Coherent_SNR = max(the_file["/lalinference/lalinference_nest/posterior_samples/L1_optimal_snr"])
        H_Coherent_SNR = max(the_file["/lalinference/lalinference_nest/posterior_samples/H1_optimal_snr"])
        fName = hdfFile[hdfFile.index("posterior_H1L1_"):]
        GPStime = hdfFile[hdfFile.index("posterior_H1L1_")+len("posterior_H1L1_"):]
        GPStime = GPStime[:GPStime.index("-")]
        the_file.close()
        outputStr = fName + '\t' + GPStime + '\t' + str(H_Coherent_SNR) + '\t' + str(L_Coherent_SNR) + '\n'
        output_file.write(outputStr)
        count+= 1
        if (count % 50 == 0):
            print ("\t "+ str(count) +'/'+ str(sizeOfList) + " complete")

    output_file.close()

    return hdfList
###############################################################################



def Incoherent_OptimalSNR(directory, num, detector):

    print("...\n" "\t Processing incoherent Data for "+detector+"...\n")

    #output file to write Optimal SNRs into
    OutputFileName = "OptSNR"+num+detector+"incoh.txt"
    output_file = open(OutputFileName, 'w')
    output_file.write("File \t GPStime \t "+ detector +"incoh"+num+'\n')

    hdfList   = []
    # Creates a list of the HDF5 file names that need to be accessed
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, "posterior_"+detector+"1_*.hdf5"):
            hdfList.append(os.path.join(root, filename))
    sizeOfList = len(hdfList)
    count = 0
    # Opens each HDF5 file needed and extracts the GPStime, H and L optimal SNR
    for hdfFile in hdfList:
        the_file = h5py.File(hdfFile,"r")
        fName = hdfFile[hdfFile.index("posterior_"+detector+"1_"):]
        GPStime = hdfFile[hdfFile.index("posterior_"+detector+"1_")+len("posterior_H1_"):]
        GPStime = GPStime[:GPStime.index("-")]
        Coherent_SNR = max(the_file["/lalinference/lalinference_nest/posterior_samples/"+detector+"1_optimal_snr"])
        the_file.close()
        outputStr = fName + '\t' + GPStime + '\t' + str(Coherent_SNR) + '\n'
        output_file.write(outputStr)
        count+= 1
        if (count % 50 == 0):
            print ("\t "+ str(count) +'/'+ str(sizeOfList) + " complete")

    output_file.close()

    return hdfList
###############################################################################




# iterating through the list of durations
for num in numList:
    Number = str(num)
    print ("Extracting the Optimal SNRs for duration " + Number + "s...")
    BASE_DIR ="/home/avi.vajpeyi/" + Folder + "/lalinferencenest/IMRPhenomPv2pseudoFourPN/"+Number+'s/posterior_samples/'

    Incoherent_OptimalSNR(BASE_DIR, Number, "H")
    Incoherent_OptimalSNR(BASE_DIR, Number, "L")
    #Coherent_OptimalSNR(BASE_DIR, Number)
