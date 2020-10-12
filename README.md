# PyOntoQuery
Retrieves information from an ontology tree.

## Dependencies (Python packages)
[obonet](https://github.com/dhimmel/obonet)  —  Read OBO-formatted ontologies in Python.  
[networkx](https://networkx.github.io/)  —  NetworkX is a dependency of obonet.

## Setting up environment

### With conda
The necessary packages and libraries are given in `environment.yml`. They may be installed with the conda package manager by running:

`$ conda env create --prefix ontology --file environment.yml`

Or to add the dependencies to a different conda environment:

`$ conda install -c biobuilds obonet`

### Without conda

#### obonet
Install the latest release of obonet from PyPI:

`$ pip install obonet`

#### NetworkX
Install the latest version of NetworkX:

`$ pip install networkx`

Install with all optional dependencies:

`$ pip install networkx[all]`
