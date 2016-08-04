
import h5py
import numpy as np
from scipy import sparse as sp
import os
import fnmatch

directory = "/home/avi.vajpeyi/backgroundAnalysis300July14/lalinferencenest/IMRPhenomPv2pseudoFourPN/8s/posterior_samples/"

hdfList   = []
for root, dirnames, filenames in os.walk(directory):
    for filename in fnmatch.filter(filenames, 'posterior_H1L1*.hdf5'):
        hdfList.append(os.path.join(root, filename))

for hdfFile in hdfList:
    the_file = h5py.File(hdfFile,"r")
    bayesFactor = the_file["/lalinference/lalinference_nest/"].attrs.get('log_bayes_factor')
    print(bayesFactor)
    the_file.close()
