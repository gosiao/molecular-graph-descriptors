# Molecular Graph Descriptors

This repository contains the modified `molecular-graph-descriptors` code (available [here](https://github.com/gosiao/molecular-graph-descriptors)).

A list of modifications:

* TODO 

It was used to generate the following data:

* [Exploration of the electron density and bare nuclear potential along the selected normal modes of the selected water clusters - W6](https://zenodo.org/records/13765791)


## Original code

The original code is available [here](https://github.com/exalearn/molecular-graph-descriptors), and accompanies the paper [A Look Inside the Black Box: Using Graph-Theoretical Descriptors to Interpret a Continuous-Filter Convolutional Neural Network (CF-CNN) trained on the Global and Local Minimum Energy Structures of Neutral Water Clusters](https://aip.scitation.org/doi/10.1063/5.0009933).

Molecular graphs and structures of over 5 million water clusters can be found [here](https://sites.uw.edu/wdbase/).


## How to test the modified code

It is best to execute the code in the `conda` environment (yaml file is available in `tests/setup/conda_env.yml`):

```
cd tests/setup
mamba env create -n molgraphdesc_env -f conda_env.yml
conda activate molgraphdesc_env
cd analysis
```

To te

## Contents

### data

.xyz files of the lowest-energy structure of each cluster size *N*=3-30 and a set of 15 clusters and their predited potential energy.

The formatted database for the 500k training and test sets used to train the published model can be obtained here: https://drive.google.com/file/d/1ZQNOhJnz0k_UWxc-CIIkYwE2d5o230Ad/view?usp=sharing

### graphdescriptors

Code for generating graphs from molecular structures and computing various descriptors from .xyz files output from SchNetPack. The script get_descriptors.py collects a set of descriptors for all molecules in the .xyz file and outputs a csv file.

A generic command to run the code is:

```
cd graphdescriptors
python get_descriptors.py --data_path ../data/test_predictions.xyz --output test_df.csv --min_dir ../data/
```



With this environment activated, to run the above command on test data:

```
./run_all.sh
```

and to run the code for extracting selected descriptors for a single structure:

```
./run_single.sh
```

The results are in the generated `results` directory.
Compare the outputs with the ones in `reference` directory.


#### Data analysis

Data analysis is in the `analysis` directory. All scripts present there should be executed in conda environment:

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


* Original code is from [this paper](https://aip.scitation.org/doi/10.1063/5.0009933):
    * Jenna A. Bilbrey, Joseph P. Heindel, Malachi Schram, Pradipta Bandyopadhyay,  Sotiris S. Xantheas, and Sutanay Choudhury. "A look inside the black box: Using graph-theoretical descriptors to interpret a Continuous-Filter Convolutional Neural Network (CF-CNN) trained on the global and local minimum energy structures of neutral water clusters" *J. Chem. Phys.* **153**, 024302 (2020).
    * BibTex:

        ```
        @article{Bilbrey2020Descriptors,
        author = {Bilbrey,Jenna A.  and Heindel,Joseph P.  and Schram,Malachi  and Bandyopadhyay,Pradipta  and Xantheas,Sotiris S.  and Choudhury,Sutanay },
        title = {A look inside the black box: Using graph-theoretical descriptors to interpret a Continuous-Filter Convolutional Neural Network (CF-CNN) trained on the global and local minimum energy structures of neutral water clusters},
        journal = {The Journal of Chemical Physics},
        volume = {153},
        number = {2},
        pages = {024302},
        year = {2020},
        doi = {10.1063/5.0009933}
        }
        ```


