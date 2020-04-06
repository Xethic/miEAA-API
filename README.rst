miEAA Command Line Interface and API
====================================

The miRNA Enrichment Analysis and Annotation Tool (miEAA) facilitates the functional analysis of miRNA sets.
This package provides a miEAA REST API wrapper and command line interface.
As such, a stable internet connection is required to utilize these tools.

| To learn more about miEAA or to utilize our online interface, please visit our `web server <https://www.ccb.uni-saarland.de/mieaa2>`_.
| All miEAA tools are provided and hosted by the `Chair for Clinical Bioinformatics at Saarland University <https://www.ccb.uni-saarland.de/>`_.
| Source code is available on `GitHub <https://github.com/Xethic/miEAA-API>`_.
| Documentation is available on `Read the Docs <https://mieaa.readthedocs.io/en/latest/>`_.


Users can execute miEAA commands directly from the command line:

.. code::

   $ mieaa -h


A REST API is also provided for scripting purposes:

.. code-block:: python

   from mieaa import API

   mieaa_api = API()
