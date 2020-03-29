miEAA
=====

The miRNA Enrichment Analysis and Annotation Tool (miEAA) facilitates the functional analysis of sets of miRNAs.
This package provides a miEAA command line and API interface.

| To learn more about miEAA or to utilize our online interface, please visit our `web server <https://www.ccb.uni-saarland.de/mieaa2>`_.
| All miEAA tools are provided and hosted by the `Chair for Clinical Bioinformatics at Saarland University <https://www.ccb.uni-saarland.de/>`_.
| Source code is available on `GitHub <https://github.com/Xethic/miEAA-API>`_.


Users can execute miEAA commands directly from the command line:

.. code::

   $ mieaa -h


An API is also provided for scripting purposes:

.. code-block:: python

   from mieaa import API

   mieaa_api = API()

Complete examples for both Python and R (using `reticulate <https://github.com/rstudio/reticulate>`_) are available under :ref:`examples`.

.. toctree::
   :maxdepth: 3

   install
   api
   cli
   examples
   license
