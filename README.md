# ESSD-mbm

Member-By-Member (MBM) scripts for the ESSD benchmark

## Installation

First clone the repository:

    git clone https://github.com/EUPP-benchmark/ESSD-mbm

and make git install the [Pythie](https://github.com/Climdyn/pythie) library:

    git submodule init
    git submodule update --remote
    
Additionaly, you may want to be sure that you have the correct version of this library:

    cd pythie
    git checkout 21a29a9dc91f1bcd6b4f75caf0d4dbae4a375303
    cd ..

Then you can create the [Anaconda](https://www.anaconda.com/) environment:

    conda env create -f environment.yml
    conda activate ESSD-mbm

And you are ready to use the notebooks or run the python scripts.

## Data

First, if you do not have it, get the ESSD benchmark dataset using [the download script](https://github.com/EUPP-benchmark/ESSD-benchmark-datasets). This will fetch the dataset into NetCDF files on your disk.

Then, for the present scripts, these NetCDF files of the ESSD benchmark must be available somewhere, and indicated in the variable `path_to_data` of the `config.py` module. In this file, the path to the postprocessors files (see below) and to where the output can be written may also be indicated.

## Details on the method and usage

The Member-By-Member postprocessing calibrates the ensemble forecasts by first correcting the systematic biases in the ensemble mean with a MOS technique (basically a linear regression) and subsequently rescaling the ensemble members around the corrected ensemble mean (see [Van Schaeybroeck & Vannitsem, 2015](https://doi.org/10.1002/qj.2397)). This procedure is performed in one step by finding the coefficients $\alpha$, $\beta$ and $\gamma$ in the formula

$$T^C_m (t) = \alpha (t) + \beta (t) \\, \mu^{\rm ens} (t) + \gamma (t) \\, \bar{T}^{\rm ens}_m (t)$$

which optimize the CRPS score ([Gneiting &Raftery, 2007](https://doi.org/10.1198/016214506000001437)), for each station and for each lead time $t$. The quantity $\mu^{\rm ens} (t)$ in the equation above is the ensemble mean, and $\bar{T}^{\rm ens}_m (t) = T^{\rm ens}_m (t) - \mu^{\rm ens (t)}$ is the deviation of the member $m$ from the ensemble mean. The results were obtained with the [Pythie package](https://github.com/Climdyn/pythie). In particular, optimization of the CRPS was done with the [Nelder-Mead method](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-neldermead.html?highlight=nelder), and using only one round of minimization. More details on the code and algorithms can be obtained in the [Pythie documentation](https://pythie.readthedocs.io).

Two experiments are here proposed:

* **global**: A global experiment using the full training dataset to obtain the coefficients $\alpha$, $\beta$ and $\gamma$ defined above. The relationship above is then used to correct the test dataset forecasts.
* **seasonal**: A seasonal experiment which obtain the coefficients $\alpha$, $\beta$ and $\gamma$ for each JFM, AMJ, JAS and OND seasons, for each year. This allows us to deal with effects due to the seasonality. Again, the relationship above is then used to correct the test dataset forecasts.

> **Remark:**
> Only the results of the global experiment were used for the ESSD benchmark.

### The global experiment

To run the global experiment (assuming you have downloaded the data), one simply has to run

    python ESSD-mbm-training-global.py
    
to train a unique [Pythie postprocessor](https://pythie.readthedocs.io/en/latest/files/postprocessors/MBM.html) which is then then stored in a pickle file `postprocessor-global.pickle`. This postprocessor will then be used by the script `ESSD-mbm-postprocessing-global.py` to postprocessed the test dataset:

    python ESSD-mbm-postprocessing-global.py
    
The output of the postprocessing is then available in a NetCDF file.

### The seasonal experiment

To run the seasonal experiment (assuming you have downloaded the data), one simply has to run

    python ESSD-mbm-training-seasonal.py
    
to train a [Pythie postprocessor](https://pythie.readthedocs.io/en/latest/files/postprocessors/MBM.html) for each season, and which are then stored in a pickle file `postprocessor-seasonal.pickle`. These postprocessors will then be used by the script `ESSD-mbm-postprocessing-seasonal.py` to postprocessed the test dataset:

    python ESSD-mbm-postprocessing-seasonal.py
    
The output of the postprocessing is then available in a NetCDF file.


## Testing the output

Once you have obtained the output of the scripts above, the notebooks `ESSD-mbm-test-global.ipynb` and `ESSD-mbm-test-seasonal.ipynb` are available to run some simple tests and compute the [CRPS scores](https://www.lokad.com/continuous-ranked-probability-score) of the postprocessed forecasts. To run them, simply start a Jupyter Notebook server:

    jupyter-notebook
    
and load them.

## Performance indication

On a computer with 96 Intel Xeon Gold 6126 CPU @ 2.60GHz with 96 Gb of RAM:

* Training takes roughly 20 minutes for both the global and seasonal model.
* Postprocessing the test dataset takes between 2 and 3 minutes for both the global and seasonal model.
