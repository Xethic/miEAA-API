# miEAA CLI and API Wrapper

The miRNA Enrichment Analysis and Annotation Tool (miEAA) facilitates the functional analysis of sets of miRNAs.  
This package provides a command line interface and wrapper for the miEAA API.

To learn more about miEAA or to utilize our online interface, please visit our [web server](https://www.ccb.uni-saarland.de/mieaa_tool).  
All miEAA tools are provided and hosted by the [Chair for Clinical Bioinformatics at Saarland University](https://www.ccb.uni-saarland.de/).

This package allows users to execute miEAA directly from the command line:

```
$ mieaa -h
```

An API wrapper is also provided for scripting purposes:

```Python
from mieaa import API

mieaa_api = API()
```

## Installation

Dependencies:

* Python >= 3.5
* Requests >= 2.19

#### pip

```
$ pip install mieaa
```

#### Conda [![Anaconda-Server Badge](https://anaconda.org/conda-forge/skidl/badges/installer/conda.svg)](https://conda.anaconda.org/conda-forge)
```
$ conda install -c ccb-sb mieaa
```

## Examples

For example usage, see the [example Python script](https://github.com/Xethic/miEAA-API/tree/master/examples/Python/).  
Using the [reticulate](https://github.com/rstudio/reticulate) library, users can utilize our package in R (Python installation is still required). As such, an [example R script](https://github.com/Xethic/miEAA-API/tree/master/examples/R/) is also provided.


## Command Line Interface

Commands can be invoked using `mieaa SUBCOMMAND`.  
Help and options for all subcommands can be invoked using `mieaa SUBCOMMAND -h`

|Subcommand|Description|
|-|-|
|to_precursor|Convert miRNAs to precursors|
|to_mirna|Convert precursors to miRNAs|
|convert_mirbase|Convert mirBase version|
|gsea|Run Gene Set Enrichment Analysis|
|ora|Run Over-representation Analysis|

Commands may require specifying if input is from a list of strings or a file (see `-m/M in examples, below`).  
In such cases, the flag letter is identical, with lowercase specifying string/list, and uppercase specifying a file.


### Important Notes

**Specifying precursors**  
For subcommands where you need to specify precursor or mature, mature is always assumed unless the `--precursor` (`-p`) flag is set.

**Mutually exclusive options**  
Each subcommand requires either `--mirna-set` (`-m`) or `--mirna-set-file` (`-M`) to be specified. Enrichment analyses also require similarly behaving arguments for categories, and optionally for reference sets in the case of ORA. 

* `miea SUBCOMMAND --mirna-set MIRNA [MIRNA ...]`
* `miea SUBCOMMAND --mirna-set MIRNAS_STRING`
* `miea SUBCOMMAND --mirna-set-file MIRNA_FILE`

### Converting miRNA -> precursor

* `mieaa to_precursor [-m | -M] -FLAGS`

```
$ mieaa to_precursor -m hsa-miR-20b-5p hsa-miR-144-5p --tabsep --unique
$ mieaa to_precursor -m 'hsa-miR-20b-5p,hsa-miR-144-5p' -o precursors.txt
$ mieaa to_precursor -M mirnas.txt --outfile precursors.txt
```

### Converting between precursor -> miRNA

* `mieaa to_mirna [-m | -M] -FLAGS`

```
$ mieaa to_mirna -m hsa-mir-20b hsa-mir-144 --tabsep --unique
$ mieaa to_mirna -m 'hsa-mir-20b,hsa-mir-144' -o mirnas.txt
$ mieaa to_mirna -M precursors.txt --outfile mirnas.txt
```

### Converting miRBase version

`mieaa convert_mirbase FROM_VERSION [-m | -M] -FLAGS`

```
$ mieaa convert_mirbase 16 -m hsa-miR-642b,hsa-miR-550b
$ mieaa convert_mirbase 16 --to 22 -m hsa-miR-642b hsa-miR-550b
$ mieaa convert_mirbase 16  -M version_16.txt -o version_22.txt
```

### Gene Set Enrichment Analysis (GSEA)

`mieaa gsea SPECIES [-m | -M] [-c | -C] -FLAGS`

Species can be specified as `hsa`, `mmu`, or `rno`.
The category flags (`-c -C`) behave identically to the miRNA set flags (`-m -M`).

```
$ mieaa gsea hsa --precursors -M precursors.txt -C categories.txt -o results.csv
$ mieaa gsea hsa -p -M precursors.txt -c HMDD MNDR > results.csv
$ mieaa gsea mmu -M mirnas.txt -C categories.txt --adjustment none
$ mieaa gsea rno -M mirnas.txt -C categories.txt -a bonferonni --json -o results.json
```

### Over-representation Analysis (ORA)

`mieaa ora SPECIES [-m | -M] [-c | -C] -FLAGS`

Species can be specified as `hsa`, `mmu`, or `rno`.
The category flags (`-c -C`)  and reference set flags (`-r -R`) behave identically to the miRNA set flags (`-m -M`).

```
$ mieaa ora hsa --precursors -M precursors.txt -C categories.txt > results.csv
$ mieaa ora hsa -p -M precursors.txt -c HMDD MNDR -o results.csv
$ mieaa ora hsa -p -M precursors.txt -C categories.txt -R reference.txt
$ mieaa ora mmu -M mirnas.txt -C categories.txt --adjustment none
$ mieaa ora rno -M mirnas.txt -C categories.txt -a bonferonni --json -o results.json
```

## API Wrapper

The miEAA API can be easily utilized via the `API` class.

### API Class

``` python
from mieaa import API

mieaa_api = API()
```

### Attributes
`job_id` - unique job identifier tied to this instance after starting an enrichment analysis

### Methods

#### convert_mirbase_version

```
mieaa_api.convert_mirbase_version(mirnas, from_version, to_version, input_type, to_file='', output_format='oneline')
```

*parameters*

* `mirnas` - str, list-like, or file-object
  * set of either mature miRNAs or precursors we want to convert
* `from_version` - float
  * miRBase version we want to convert given set from
* `to_version` - float
  * miRBase version we want to convert given set to
* `input_type` - 'precursor' or 'mirna'
  * Whether the provided set includes precursors or mature miRNAs
* `to_file` - file-object or str
  * If provided, converted miRNA/precursor set will be saved
* `output_format` - 'oneline' or 'tabsep'
  * 'oneline': Text containing only converted miRNAs/precursors
  * 'tabsep': Tab-separated input and output miRNAs/precursors

*return*

  `list` - converted miRNAs/precursors

#### convert_mirna_to_precursor

```
mieaa_api.convert_mirna_to_precursor(mirnas,  to_file='', output_format='oneline', conversion_type='all')
```

*parameters*

* `mirnas` - str, list-like, or file-object
  * set of either mature miRNAs or precursors we want to convert
* `to_file` - file-object or str
  * If provided, converted miRNA/precursor set will be saved
* `output_format` - 'oneline' or 'tabsep'
  * 'oneline': Text containing only converted miRNAs/precursors
  * 'tabsep': Tab-separated input and output miRNAs/precursors
* `conversion_type`: 'all' or 'unique'
  * 'all': Output all newly converted precursors
  * 'unique': Only output precursors with unique mappings

*return*

  `list` - newly converted precursors

#### convert_precursor_to_mirna

``` python
mieaa_api.convert_precursor_to_mirna(mirnas,  to_file='', output_format='oneline', conversion_type='all')
```

*parameters*

* `mirnas` - str, list-like, or file-object
  * set of either mature miRNAs or precursors we want to convert
* `to_file` - file-object or str
  * If provided, converted miRNA/precursor set will be saved
* `output_format` - 'oneline' or 'tabsep'
  * 'oneline': Text containing only converted miRNAs/precursors
  * 'tabsep': Tab-separated input and output miRNAs/precursors
* `conversion_type`: 'all' or 'unique'
  * 'all': Output all newly converted miRNAs
  * 'unique': Only output miRNAs with unique mappings

*return*

  `list` - newly converted miRNAs

#### run_gsea

``` python
mieaa_api.run_gsea(test_set, categories, input_type, species, p_value_adjustment='fdr', significance_level=0.05, independent_p_adjust=True, threshold_level=2)
```

*parameters*

* `test_set` - str, list-like, or file-object
  * set of either mature miRNAs or precursors we want to convert
* `categories` - str, list-like, or file-object
  * set of categories use in enrichment analysis
* `input_type` - 'precursor' or 'mirna'
  * Whether the provided set includes precursors or mature miRNAs
* `species` - 'hsa', 'mmu', 'rno'
  * 'hsa': Homo sapiens
  * 'mmu': Mus musculus
  * 'rno': Rattus norvegicus
* `p_value_adjustment` - 'none','fdr','bonferroni','BY','holm','hochberg','hommel'
  * 'none' - No adjustment
  * 'fdr' - FDR (Benjamini-Hochberg) adjustment
  * 'bonferroni' - Bonferroni adjustmen
  * 'BY' - Benjamini-Yekutieli adjustment
  * 'hochberg' - Hochberg adjust
  * 'holm' - Holm adjustment
  * 'hommel' - Hommel adjustment
* `significance_level` - float
  * Filter out p-values above specified level
* `independent_p_adjust` - bool
  * True: Adjust p-values for each category independently
  * False: Adjust p-values for all categories collectively
* `threshold_level` - int
  * Filter out subcategories containing less than this many miRNAs/precursors

*return*

  `requests.Response` - API response

#### run_ora

``` python
mieaa_api.run_ora(test_set, categories, input_type, species, reference_set='', p_value_adjustment='fdr', significance_level=0.05, independent_p_adjust=True, threshold_level=2)
```

*parameters*

* `test_set` - str, list-like, or file-object
  * set of either mature miRNAs or precursors we want to convert
* `categories` - str, list-like, or file-object
  * set of categories use in enrichment analysis
* `input_type` - 'precursor' or 'mirna'
  * Whether the provided set includes precursors or mature miRNAs
* `species` - 'hsa', 'mmu', 'rno'
  * 'hsa': Homo sapiens
  * 'mmu': Mus musculus
  * 'rno': Rattus norvegicus
* `reference_set` - str, list-like, or file-object
  * If specified, use as background reference set
* `p_value_adjustment` - 'none','fdr','bonferroni','BY','holm','hochberg','hommel'
  * 'none' - No adjustment
  * 'fdr' - FDR (Benjamini-Hochberg) adjustment
  * 'bonferroni' - Bonferroni adjustmen
  * 'BY' - Benjamini-Yekutieli adjustment
  * 'hochberg' - Hochberg adjust
  * 'holm' - Holm adjustment
  * 'hommel' - Hommel adjustment
* `significance_level` - float
  * Filter out p-values above specified level
* `independent_p_adjust` - bool
  * True: Adjust p-values for each category independently
  * False: Adjust p-values for all categories collectively
* `threshold_level` - int
  * Filter out subcategories containing less than this many miRNAs/precursors

*return*

  `requests.Response` - API response

#### get_enrichment_Parameters

```
mieaa_api.get_enrichment_Parameters()
```

*return*

  `dict` - Parameters that were provided when calling `run_gsea()` or `run_ora()`

#### get_results

```
mieaa_api.get_results(results_format='json', check_progress_interval=5)
```

*parameters*

* `results_format` - 'json' or 'csv'
  * Whether to retrieve results as json or as a csv string
* `check_progress_interval` - float
  * How many seconds to wait in between checking if results have finished computing

*return*

  `list` or `str` containing the results

#### save_enrichment_results

``` python
mieaa_api.save_enrichment_results(save_file, file_type='csv', check_progress_interval=5)
```

*parameters*

* `save_file` - str or file-object
  * Where to save the results
* `file_type` - 'csv' or 'json'
  * File format we want to save results as
* `check_progress_interval` - float
  * How many seconds to wait in between checking if results have finished computing

*return*

* `str` - results as they were written to file

#### invalidate
Invalidate this instance. Previous results become irretrievable, but can now be used to run a fresh analysis.

``` python
mieaa_api.invalidate()
```

*return*

None

#### get_enrichment_categories

```
mieaa_api.get_enrichment_categories(input_type, species, with_suffix=False)
```

*parameters*

* `input_type` - 'precursor' or 'mirna'
  * Whether the provided set includes precursors or mature miRNAs
* `species` - 'hsa', 'mmu', 'rno'
  * 'hsa': Homo sapiens
  * 'mmu': Mus musculus
  * 'rno': Rattus norvegicus
* `with_suffix` - bool
  * Whether to include '_precursor' or '_mature' suffix in category names
  
*return*
  `dict` - keys are the category names, values are a short description
