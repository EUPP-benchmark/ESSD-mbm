# ESSD-mbm

MBM scripts for the ESSD benchmark

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

The data files of the ESSD benchmark must be available somewhere, and indicated in the variable `path_to_data` of the `config.py` module. In this file, the path to the postprocessors files and to where the output can be written may also be indicated.

## Usage

In a terminal, you can launch the python scripts with `training` in their name to train the postprocessors. The `postprocessing` scripts can then be also launched to obtain the postprocessed forecasts as netCDF files.

## Details on the method

The Member-By-Member postprocessing calibrates the ensemble forecasts by first correcting the systematic biases in the ensemble mean with a MOS technique (basically a linear regression) and subsequently rescaling the ensemble members around the corrected ensemble mean (see [Van Schaeybroeck & Vannitsem, 2015](https://doi.org/10.1002/qj.2397)). This procedure is performed in one step by finding the coefficients $\alpha$, $\beta$ and $\gamma$ in the formula

$$T^C_m (t) = \alpha (t) + \beta (t) \, \mu^{\rm ens} (t) + \gamma (t) \, \bar{T}^{\rm ens}_m (t)$$

which optimize the CRPS score ([Gneiting &Raftery, 2007](https://doi.org/10.1198/016214506000001437)), for each station and for each lead time $t$. The quantity $\mu^{\rm ens} (t)$ in the equation above is the ensemble mean, and $\bar{T}^{\rm ens}_m (t) = T^{\rm ens}_m (t) - \mu^{\rm ens (t)}$ is the deviation of the member $m$ from the ensemble mean. The results were obtained with the [Pythie package](https://github.com/Climdyn/pythie). In particular, optimization of the CRPS was done with the [Nelder-Mead method](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-neldermead.html?highlight=nelder), and using only one round of minimization.

## Testing the output
