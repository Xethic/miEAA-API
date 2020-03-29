# miEAA CLI and API

The miRNA Enrichment Analysis and Annotation Tool (miEAA) facilitates the functional analysis of sets of miRNAs.  
This package provides a miEAA command line and API interface.

To learn more about miEAA or to utilize our online interface, please visit our [web server](https://www.ccb.uni-saarland.de/mieaa2).  
All miEAA tools are provided and hosted by the [Chair for Clinical Bioinformatics at Saarland University](https://www.ccb.uni-saarland.de/).

This package allows users to execute miEAA directly from the command line:

```
$ mieaa -h
```

An API is also provided for scripting purposes:

```Python
from mieaa import API

mieaa_api = API()
```

## Documentation

Thorough documentation for the miEAA CLI and API is available on [Read the Docs](https://mieaa.readthedocs.io/en/latest/)

## Examples

For example usage, see the [example Python script](https://github.com/Xethic/miEAA-API/tree/master/examples/Python/). 

For R, users can utilize the [reticulate](https://github.com/rstudio/reticulate) library (Python installation is still required). An [example R script](https://github.com/Xethic/miEAA-API/tree/master/examples/R/) is provided using this method.
