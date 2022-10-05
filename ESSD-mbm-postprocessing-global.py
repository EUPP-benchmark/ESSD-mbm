#!/usr/bin/env python
# coding: utf-8

# ## Preliminaries

# Timestamping

# In[ ]:


import time
import datetime
print('Starting postprocessing at:')
print(datetime.datetime.now())
start_time = time.time()
print('\n')


# Setting the path

# In[ ]:


import sys, os
sys.path.extend([os.path.abspath('./pythie')])


# Importing external modules

# In[ ]:


import pickle
import matplotlib.pyplot as plt
import numpy as np


# In[ ]:


import xarray as xr


# Importing internal modules

# In[ ]:


from core.data import Data
import postprocessors.MBM as MBM
import config


# ## Loading the data

# Loading with xarray

# In[ ]:


fcs_data = xr.open_dataarray(config.path_to_data + 'ESSD_benchmark_test_data_forecasts.nc')
obs_data = xr.open_dataarray(config.path_to_data + 'ESSD_benchmark_test_data_observations.nc')


# Transposing to agree with Pythie data model

# In[ ]:


fcs_data = fcs_data.transpose('time', 'number', 'step', 'station_id')
obs_data = obs_data.transpose('time', 'step', 'station_id')


# ## Postprocessing

# In[ ]:


with open('postprocessor-global.pickle', 'rb') as fo:
    postprocessor = pickle.load(fo)


# In[ ]:


# converting to numpy arrays in °C
fcs = fcs_data.to_numpy() - 273.15
obs = obs_data.to_numpy() - 273.15

# arranging all the forecasts to fit the Pythie data model
fcs = fcs.reshape((1, fcs.shape[0], fcs.shape[1], 1, fcs.shape[2], fcs.shape[3], 1))
obs = obs.reshape((1, obs.shape[0], 1, 1, obs.shape[1], obs.shape[2], 1))

# creating the pythie data
data_t2_fcs = Data(fcs)
data_t2_obs = Data(obs)

# postprocessing and saving the result
corr_data_t2_fcs = postprocessor(data_t2_fcs)


# ## Plotting the results of a given season

# Uncomment to check

# In[ ]:


# raw_crps = data_t2_fcs.CRPS(data_t2_obs)


# In[ ]:


# corr_crps = corr_data_t2_fcs.CRPS(data_t2_obs)


# In[ ]:


# fig = plt.figure(figsize=(12,10))
# ax = fig.gca()
# corr_crps.plot(grid_point=(200,0), ax)
# raw_crps.plot(grid_point=(200,0), ax=ax)


# ## Converting the postprocessed forecasts back to netCDF

# Creating a new forecasts xarray and updating it with the corrected forecasts

# In[ ]:


corrected_fcs_data = fcs_data.copy()


# In[ ]:


# also converting back to °K
corrected_fcs_data.data = np.squeeze(corr_data_t2_fcs_total.data) + 273.15


# Deleting useless attributes for the benchmark

# In[ ]:


fcs_attrs_keys = list(corrected_fcs_data.attrs.keys())

for key in fcs_attrs_keys:
    if 'GRIB' in key:
        del corrected_fcs_data.attrs[key]


del corrected_fcs_data.attrs['coordinates']
del corrected_fcs_data.attrs['standard_name']
del corrected_fcs_data.attrs['model altitude source']
del corrected_fcs_data.attrs['land usage source']
del corrected_fcs_data.attrs['land usage legend']


# Updating the attributes to identify the output dataset

# In[ ]:


attrs = dict()
# the current ESSD benchmark is the Tier 1 of the hacky benchmark
# by the definition given here: https://portal.eumetnet.eu/display/PBM/Benchmark+Hacky+Phase+Tiers+Organization
attrs['tier'] = '1'  
attrs['experiment'] = 'ESSD-benchmark'
attrs['institution'] = 'RMIB'
attrs['model'] = 'Pythie-MBM-AbsCRPSmin-global'
attrs['model_version'] = 'commit 21a29a9dc91f1bcd6b4f75caf0d4dbae4a375303'

corrected_fcs_data.attrs.update(attrs)


# Transposing back to the input dataset format

# In[ ]:


corrected_fcs_data = corrected_fcs_data.transpose('station_id', 'time', 'step', 'number')


# Writing to file in netCDF4 format

# In[ ]:


# filename is "<tier>_<experiment>_<institution>_<model>_<version>.nc"
del attrs['model_version']  # not needed in the filename
file_info = '_'.join(attrs.values())
file_name = config.path_to_output + file_info + '.nc'
print('Saving the result to ' + file_name + ' ...')
corrected_fcs_data.to_netcdf(file_name)


# ## Plotting a given corrected forecast

# Uncomment to check

# In[ ]:


# fig = plt.figure(figsize=(12,10))
# ax = fig.gca()
# fcs_data.isel(station_id=200,number=0,time=0).plot(ax=ax, label='raw')
# corrected_fcs_data.isel(station_id=200,number=0,time=0).plot(ax=ax, label='corrected')
# plt.legend()


# ## Final timing

# In[ ]:


print('Postprocessing finished at:')
print(datetime.datetime.now())
end_time = time.time()
print('Time elapsed:')
print(str((end_time - start_time) / 60) + ' minutes elapsed.')

