
import h5py
import numpy as np
from scipy import sparse as sp
import os
import fnmatch


"""
directory = "/home/avi.vajpeyi/backgroundAnalysis300July14/lalinferencenest/IMRPhenomPv2pseudoFourPN/8s/posterior_samples/"

hdfList   = []

# Creates a list of the HDF5 file names that need to be accessed
for root, dirnames, filenames in os.walk(directory):
    for filename in fnmatch.filter(filenames, 'posterior_H1L1*.hdf5'):
        hdfList.append(os.path.join(root, filename))

# Opens each HDF5 file needed and extracts the bayes factor from it
for hdfFile in hdfList:
    the_file = h5py.File(hdfFile,"r")
    bayesFactor = the_file["/lalinference/lalinference_nest/"].attrs.get('log_bayes_factor')
    print(bayesFactor)
    the_file.close()
"""


fn = 'H1L1-STATMAP_FULL_DATA_FULL_CUMULATIVE_CAT_12H_FULL_DATA_FULL_BIN_2-1126051217-3331800.hdf'
trigs = h5py.File(fn, 'r')
#trigs.keys() gives:
#[u'background', u'background_exc', u'foreground', u'segments']
#
#trig.attrib.keys() gives
#[u'detector_1', u'detector_2', u'timeslide_interval', u'background_time', u'foreground_time', u'background_time_exc', u'foreground_time_exc', u'name']
#
#
#trigs.attrs['detector_1'] gives
# 'H1'


bg = trigs['background_exc']
#bg.keys() gives
#[u'decimation_factor', u'ifar', u'stat', u'template_id', u'time1', u'time2', u'timeslide_id', u'trigger_id1', u'trigger_id2']
# here bg['time1'] ---> GPS time in detector 1 (H)
#      bg['ifar']  ---> Inverse FAR
"""
print(bg['time1'])
bg['time1'][:]

trigs.attrs.keys()
trigs.attrs['detector_1']
"""

# Access the ifar and print those out.
# Access the GPS time in H and L which are bg['time1'] bg['time2']
# Access the trigger ID for both
# Access the SNR
# Access the LnL


OutputFileName = "pycbcBackgroundData.txt"
# File to output coherent data in
output_file = open(OutputFileName, 'w')
output_file.write("H_time \t L_time \t SNR \t iFAR \n" )


print("Copying H data...")
H_time = bg['time1'][:]
print("Copying L data...")
L_time = bg['time2'][:]
print("Copying SNR data...")
SNRval = bg['stat'][:]
print("Copying iFAR data...")
ifar   = bg['ifar'][:]

print("Saving data to files...")
for i in range(len(ifar)):
    outputStr = str(H_time[i]) + '\t' + str(L_time[i]) + '\t' + str(SNRval[i]) + '\t' + str(ifar[i]) + '\n'
    output_file.write(outputStr)
output_file.close()
