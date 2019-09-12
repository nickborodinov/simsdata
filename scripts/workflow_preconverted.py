﻿# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 15:26:08 2016

@author: iv1
"""
import datetime

#%%This code won’t work from Python console
#!!! Clean import procedure with __init__.py file etc.
from SIMSmodel import SIMSmodel
from SIMSdata import SIMSdata
import os
verbose = True
#%%

#print('start time = %s'%(str(timestamps['start'])))
if __name__ == '__main__':

    cores = 8
    #Path to file and prefix
    path = r'G:\kick-ass brain data\SIMS'
    prefix = '001 stage scan mouse brain'
    #Initialize converter class
    if verbose:
        print('Initializing data handler...')
    sims_data = SIMSdata()
    h5_path = os.path.join(path, prefix+'.h5')
    sims_data.load_h5(h5_path)

    #Preparing SIMS conversion model
    if verbose:
        print('Intiailizing data converter...')
    model = SIMSmodel(xy_bins=1, z_bins=3, counts_threshold=1000000, tof_resolution=64) #Minimal overhead

    model.convert_all_peaks()
    #model.enable_shift_correction()
    if verbose:
        print('Converting data...')
    data2d = sims_data.convert_data('all', model, cores)
    if verbose:
        print('Loading converted data...')
    sims_data.load_converted_data(1)
    if verbose:
        print('Calculating PCA...')
    sims_data.PCA(comp_num=20, spatial_range=(slice(30), -1, -1))
    if verbose:
        print('Calculating NMF...')
    sims_data.NMF(20)

    #Plotting averaged data
    #sims_data.plot_ave_data()
    if verbose:
        print('Finished converting, closing model.')
    sims_data.close()