# PyOntoQuery
A Python command line utility that retrieves information from an ontology tree (.obo) file.

#### **Note: if you are installing this on Eddie (the University of Edinburgh's cluster) it seems you will need to follow the 'Without conda' instructions for now**

## Downloading this git repository

You can download the contents of this `git` repository by running:

`git clone https://github.com/baileythegreen/PyOntoQuery.git`

This assumes you have `git` installed. Or, you can click on the **Code** button in the top right-ish part of this page, next to the **About** section and choose **Download ZIP**, which does not.

## Dependencies (Python packages)
[obonet](https://github.com/dhimmel/obonet)  —  Read OBO-formatted ontologies in Python.  
[networkx](https://networkx.github.io/)  —  NetworkX is a dependency of obonet.

## Setting up environment

### With conda

#### Setting up the environment
The necessary packages and libraries are given in `environment.yml`. They may be installed with the conda package manager by running:

`$ conda env create --prefix ontology --file environment.yml`

creates an 'ontology' environment in the current directory, or

`$ conda env create --prefix /path/to/another/location/ontology --file environment.yml`

creates the environment in another location.

#### Activating the environment
You can activate this environment with:

`$ conda activate ./ontology`

if the environment is in your current directory, or

`$ conda activate <path to where ever you created it>/ontology`

if it is not.


#### Adding PyOntoQuery to an existing conda environment
Or to add the dependencies to a different (already extant) conda environment:

`$ conda install -c biobuilds obonet`

(This line will install obonet and all of its dependencies, which will then be everything you need.)

### Without conda

#### obonet
Install the latest release of obonet from PyPI:

`$ pip install obonet`

#### NetworkX
Install the latest version of NetworkX:

`$ pip install networkx`

Install with all optional dependencies:

`$ pip install networkx[all]`
