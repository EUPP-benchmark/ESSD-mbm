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

