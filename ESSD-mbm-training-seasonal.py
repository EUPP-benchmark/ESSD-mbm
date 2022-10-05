#!/usr/bin/env python
# coding: utf-8

# ## Preliminaries

# Timestamping

# In[ ]:


import time
import datetime
print('Starting training at:')
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


rfcs_data = xr.open_dataarray(config.path_to_data + 'ESSD_benchmark_training_data_forecasts.nc')
robs_data = xr.open_dataarray(config.path_to_data + 'ESSD_benchmark_training_data_observations.nc')


# Transposing to agree with Pythie data model

# In[ ]:


rfcs_data = rfcs_data.transpose('time', 'year', 'number', 'step', 'station_id')
robs_data = robs_data.transpose('time', 'year', 'step', 'station_id')


# ## Setting the season indices

# In[ ]:


season_index = dict()
season_index[2017] = {'JFM': slice('2017-01-01', '2017-03-31'),
                      'AMJ': slice('2017-04-01', '2017-06-30'),
                      'JAS': slice('2017-07-01', '2017-09-30'),
                      'OND': slice('2017-10-01', '2017-12-31')
                     }

season_index[2018] = {'JFM': slice('2018-01-01', '2018-03-31'),
                      'AMJ': slice('2018-04-01', '2018-06-30'),
                      'JAS': slice('2018-07-01', '2018-09-30'),
                      'OND': slice('2018-10-01', '2018-12-31')
                     }


# ## Looping on the seasons and training the Pythie postprocessor objects

# In[ ]:


postprocessors = dict()
postprocessors[2017] = dict()
postprocessors[2018] = dict()

for year in season_index:
    for season in season_index[year]:
        print('Training of season '+season+str(year)+' started at:')
        print(datetime.datetime.now())
        print('...')
        
        # selecting the season's data
        rfcs = rfcs_data.sel(time=season_index[year][season])
        robs = robs_data.sel(time=season_index[year][season])
        
        # converting to numpy arrays in °C
        rfcs = rfcs.to_numpy() - 273.15
        robs = robs.to_numpy() - 273.15
        
        # arranging all the reforecasts of different years along a single axis
        rfcs = rfcs.reshape((rfcs.shape[0]*rfcs.shape[1], rfcs.shape[2], 1, rfcs.shape[3], rfcs.shape[4]))
        robs = robs.reshape((robs.shape[0]*robs.shape[1], 1, 1, robs.shape[2], robs.shape[3]))
        
        # creating the pythie data model
        data_t2_fcs = Data(rfcs[np.newaxis, ..., np.newaxis])
        data_t2_obs = Data(robs[np.newaxis, ..., np.newaxis])
        
        # creating and training a Pythie postprocessor
        postprocessor = MBM.EnsembleAbsCRPSCorrection()
        postprocessor.train(data_t2_obs, data_t2_fcs, ntrial=1)
        
        postprocessors[year][season] = postprocessor
        print('Training of season finished at:')
        print(datetime.datetime.now())
        print('\n')
        


# ## Storing the output

# In[ ]:


with open(config.path_to_postprocessors + 'postprocessors-seasonal.pickle', 'wb') as fo:
    pickle.dump(postprocessors, fo)


# ## Plotting the results with the last postprocessor

# Uncomment to check

# In[ ]:


# postprocessor.plot_parameters(grid_point=(200,0))


# In[ ]:


# raw_crps = data_t2_fcs.CRPS(data_t2_obs)


# In[ ]:


# corr = postprocessor(data_t2_fcs)


# In[ ]:


# corr_crps = corr.CRPS(data_t2_obs)


# In[ ]:


# ax = corr_crps.plot(grid_point=(200,0))
# raw_crps.plot(grid_point=(200,0), ax=ax)


# ## Final timing

# In[ ]:


print('Training of all season finished at:')
print(datetime.datetime.now())
end_time = time.time()
print('Time elapsed:')
print(str((end_time - start_time) / 60) + ' minutes elapsed.')

