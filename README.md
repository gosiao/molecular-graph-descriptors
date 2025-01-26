# Molecular Graph Descriptors

This repository contains the modified `molecular-graph-descriptors` code (available [here](https://github.com/gosiao/molecular-graph-descriptors)).

It was used to generate the following data:

* [Exploration of the electron density and bare nuclear potential along the selected normal modes of the selected water clusters - W6](https://zenodo.org/records/13765791)

The extensions of the original code are covered by tests (described below).


## Contents of this repository

### data

This directory contains the selected XYZ files with geometries of water clusters.

In addition to the original data (https://github.com/exalearn/molecular-graph-descriptors/tree/master/data), the `water_selected_5kcalmol/` subdirectory contains the subset of the `wdbase` used for testing.

### graphdescriptors

Code for generating graphs from molecular structures and computing various descriptors from .xyz files output from SchNetPack. The script get_descriptors.py collects a set of descriptors for all molecules in the .xyz file and outputs a csv file.

A generic command to run the code is:

```
cd graphdescriptors
python get_descriptors.py --data_path ../data/test_predictions.xyz --output test_df.csv --min_dir ../data/
```


## How to test the modified code

It is best to execute the code in the `conda` environment (yaml file is available in `tests/setup/conda_env.yml`).
To create and activate the environment, run:

```
cd tests/setup
mamba env create -n molgraphdesc_env -f conda_env.yml
conda activate molgraphdesc_env
cd analysis
```

With this environment activated:

* to test the capabilities of the original code, execute:

```
./run_all.sh
```

* to test the code for extracting the selected descriptors for a single structure:

```
./run_single.sh
```

* to calculate the graph similarity between two structures:

```
./run_similarity.sh
```


The results are in the generated `results` directory.
Compare the outputs with the ones in `reference` directory.


### Additional analysis tools

This is WIP.

Data analysis is in the `analysis` directory.
All scripts present there should be executed in conda environment; a sample workflow is presented in the jupyter notebook.

Additional functionalities for running the analysis in the jupyter notebooks:

```
jupyter labextension install jupyterlab_3dmol
```

```
cd analysis
```

To select the structures from the original pool, modify and run:

```
python analysis_initial.py
```


To analyze the structures after the geometry reoptimization, modify and run:


```
python analysis_geomopt.py
```





## References


### Original code

The original code is available [here](https://github.com/exalearn/molecular-graph-descriptors), and accompanies the paper [A Look Inside the Black Box: Using Graph-Theoretical Descriptors to Interpret a Continuous-Filter Convolutional Neural Network (CF-CNN) trained on the Global and Local Minimum Energy Structures of Neutral Water Clusters](https://aip.scitation.org/doi/10.1063/5.0009933).

Molecular graphs and structures of over 5 million water clusters can be found [here](https://sites.uw.edu/wdbase/).



