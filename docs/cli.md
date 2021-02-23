# Command Line Interface

Commands can be invoked via the command line using `mieaa SUBCOMMAND`.  
Help and options for all subcommands can be view with `mieaa SUBCOMMAND -h`


**Supported Species**  
  * *hsa* - Homo sapiens
  * *mmu* - Mus musculus
  * *rno* - Rattus norvegicus
  * *ath* - Arabidopsis thaliana
  * *bta* - Bos taurus
  * *cel* - Caenorhabditis elegans
  * *dme* - Drosophila melanogaster
  * *dre* - Danio rerio
  * *gga* - Gallus gallus
  * *ssc* - Sus scrofa

**Specifying precursors**  
For subcommands where you need to specify precursor or mature, mature is always assumed unless the `--precursor` (`-p`) flag is set.

**Mutually exclusive options**  
Most subcommands require one of `--mirna-set` (`-m`) or `--mirna-set-file` (`-M`) to be specified.

* `mieaa SUBCOMMAND --mirna-set MIRNA [MIRNA ...]`
* `mieaa SUBCOMMAND --mirna-set MIRNAS_STRING`
* `mieaa SUBCOMMAND --mirna-set-file MIRNA_FILE`

## Subcommands

### to_precursor

Convert miRNA -> precursor

```
usage: miEAA to_precursor [-h] [-v] [-m MIRNA_SET [MIRNA_SET ...]]
                          [-M MIRNA_SET_FILE] [-p] [-o OUTFILE]
                          [--oneline | --newline | --tabsep] [-u]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Always print results to stdout
  -p, --precursor, --precursors
                        Use if running on a set of precursors as opposed to
                        miRNAs
  -o OUTFILE, --outfile OUTFILE
                        Save results to provided file
  --oneline             Output style: Multi-mapped ids are separated by a
                        semicolon (default)
  --newline             Output style: Multi-mapped ids are separated by a
                        newline
  --tabsep              Output style: Tab-separated `original converted` ids
  -u, --unique          Only output ids that map uniquely

mutually exclusive required arguments:
  either a set or file must be provided

  -m MIRNA_SET [MIRNA_SET ...], --mirna-set MIRNA_SET [MIRNA_SET ...]
                        miRNA/precursor target set
  -M MIRNA_SET_FILE, --mirna-set-file MIRNA_SET_FILE
                        Specify miRNA/precursor target set via file
```

Examples:

```
$ mieaa to_precursor -m hsa-miR-20b-5p hsa-miR-144-5p --tabsep --unique
$ mieaa to_precursor -m 'hsa-miR-20b-5p,hsa-miR-144-5p' --newline -o precursors.txt
$ mieaa to_precursor -M mirnas.txt --outfile precursors.txt
```

### to_mirna

Converting between precursor -> miRNA

```
usage: miEAA to_mirna [-h] [-v] [-m MIRNA_SET [MIRNA_SET ...]]
                      [-M MIRNA_SET_FILE] [-p] [-o OUTFILE]
                      [--oneline | --newline | --tabsep] [-u]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Always print results to stdout
  -p, --precursor, --precursors
                        Use if running on a set of precursors as opposed to
                        miRNAs
  -o OUTFILE, --outfile OUTFILE
                        Save results to provided file
  --oneline             Output style: Multi-mapped ids are separated by a
                        semicolon (default)
  --newline             Output style: Multi-mapped ids are separated by a
                        newline
  --tabsep              Output style: Tab-separated `original converted` ids
  -u, --unique          Only output ids that map uniquely

mutually exclusive required arguments:
  either a set or file must be provided

  -m MIRNA_SET [MIRNA_SET ...], --mirna-set MIRNA_SET [MIRNA_SET ...]
                        miRNA/precursor target set
  -M MIRNA_SET_FILE, --mirna-set-file MIRNA_SET_FILE
                        Specify miRNA/precursor target set via file
```

Examples:

```
$ mieaa to_mirna -m hsa-mir-20b hsa-mir-144 --tabsep --unique
$ mieaa to_mirna -m 'hsa-mir-20b,hsa-mir-144' --newline -o mirnas.txt
$ mieaa to_mirna -M precursors.txt --outfile mirnas.txt
```

### convert_mirbase

Converting miRBase version

```
usage: miEAA convert_mirbase [-h] [-v] [-m MIRNA_SET [MIRNA_SET ...]]
                             [-M MIRNA_SET_FILE] [-p] [-o OUTFILE]
                             [--oneline | --newline | --tabsep] [--to TO]
                             FROM

positional arguments:
  FROM                  mirBase version to convert miRNAs/precursors from

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Always print results to stdout
  -p, --precursor, --precursors
                        Use if running on a set of precursors as opposed to
                        miRNAs
  -o OUTFILE, --outfile OUTFILE
                        Save results to provided file
  --oneline             Output style: Multi-mapped ids are separated by a
                        semicolon (default)
  --newline             Output style: Multi-mapped ids are separated by a
                        newline
  --tabsep              Output style: Tab-separated `original converted` ids
  --to TO               mirBase version to convert miRNAs/precursors from
                        (default=22)

mutually exclusive required arguments:
  either a set or file must be provided

  -m MIRNA_SET [MIRNA_SET ...], --mirna-set MIRNA_SET [MIRNA_SET ...]
                        miRNA/precursor target set
  -M MIRNA_SET_FILE, --mirna-set-file MIRNA_SET_FILE
                        Specify miRNA/precursor target set via file
```

Examples:

```
$ mieaa convert_mirbase 16 -m hsa-miR-642b,hsa-miR-550b
$ mieaa convert_mirbase 16 --to 22 -m hsa-miR-642b hsa-miR-550b
$ mieaa convert_mirbase 16  -M version_16.txt -o version_22.txt
```

### gsea

Gene Set Enrichment Analysis (GSEA)

```
usage: miEAA gsea [-h] [-v] [-m MIRNA_SET [MIRNA_SET ...]] [-M MIRNA_SET_FILE]
                  [-p] [-o OUTFILE] [-x] [-c CATEGORIES [CATEGORIES ...]]
                  [-C CATEGORIES_FILE] [-t THRESHOLD] [-s SIGNIFICANCE] [-g]
                  [-a {none,fdr,bonferroni,BY,holm,hochberg,hommel}]
                  [--csv | --json]
                  {hsa,mmu,rno,ath,bta,cel,dme,dre,gga,ssc}

positional arguments:
  {hsa,mmu,rno,ath,bta,cel,dme,dre,gga,ssc}
                        Species

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Always print results to stdout
  -p, --precursor, --precursors
                        Use if running on a set of precursors as opposed to
                        miRNAs
  -o OUTFILE, --outfile OUTFILE
                        Save results to provided file
  -x, --no-results      Do not monitor progress or obtain results. Can
                        retrieve later using Job ID.
  -t THRESHOLD, --threshold THRESHOLD
                        Filter out subcategories that contain less than this
                        many miRNAs/precursors (default=2)
  -s SIGNIFICANCE, --significance SIGNIFICANCE, --alpha SIGNIFICANCE
                        Significance level (default=0.05)
  -g, --group-adjust    Adjust p-values over aggregated groups (By default
                        each group is adjusted independently)
  -a {none,fdr,bonferroni,BY,holm,hochberg,hommel}, --adjustment {none,fdr,bonferroni,BY,holm,hochberg,hommel}
                        p-value adjustment method (default='fdr')
  --csv                 Store results in output file in csv format (default)
  --json                Store results in output file in json format (default
                        is csv)

mutually exclusive required arguments:
  either a set or file must be provided

  -m MIRNA_SET [MIRNA_SET ...], --mirna-set MIRNA_SET [MIRNA_SET ...]
                        miRNA/precursor target set
  -M MIRNA_SET_FILE, --mirna-set-file MIRNA_SET_FILE
                        Specify miRNA/precursor target set via file

mutually exclusive optional arguments:
  either a set or file may be provided

  -c CATEGORIES [CATEGORIES ...], --categories CATEGORIES [CATEGORIES ...]
                        Set of categories to include in analysis, can include
                        `all`, `default`, `expert` or specific categories
  -C CATEGORIES_FILE, --categories-file CATEGORIES_FILE
                        File specifying categories to include in analysis
```

Examples:

```
$ mieaa gsea hsa --precursors -M precursors.txt -C categories.txt -o results.csv
$ mieaa gsea hsa -p -M precursors.txt -c HMDD MNDR > results.csv
$ mieaa gsea mmu -M mirnas.txt -C categories.txt --adjustment none
$ mieaa gsea rno -M mirnas.txt -C categories.txt -a bonferroni --json -o results.json
```

### ora

Over-representation Analysis (ORA)

```
usage: miEAA ora [-h] [-v] [-m MIRNA_SET [MIRNA_SET ...]] [-M MIRNA_SET_FILE]
                 [-p] [-o OUTFILE] [-x] [-c CATEGORIES [CATEGORIES ...]]
                 [-C CATEGORIES_FILE] [-t THRESHOLD] [-s SIGNIFICANCE] [-g]
                 [-a {none,fdr,bonferroni,BY,holm,hochberg,hommel}]
                 [--csv | --json] [-r REFERENCE_SET [REFERENCE_SET ...]]
                 [-R REFERENCE_SET_FILE]
                 {hsa,mmu,rno,ath,bta,cel,dme,dre,gga,ssc}

positional arguments:
  {hsa,mmu,rno,ath,bta,cel,dme,dre,gga,ssc}
                        Species

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Always print results to stdout
  -p, --precursor, --precursors
                        Use if running on a set of precursors as opposed to
                        miRNAs
  -o OUTFILE, --outfile OUTFILE
                        Save results to provided file
  -x, --no-results      Do not monitor progress or obtain results. Can
                        retrieve later using Job ID.
  -t THRESHOLD, --threshold THRESHOLD
                        Filter out subcategories that contain less than this
                        many miRNAs/precursors (default=2)
  -s SIGNIFICANCE, --significance SIGNIFICANCE, --alpha SIGNIFICANCE
                        Significance level (default=0.05)
  -g, --group-adjust    Adjust p-values over aggregated groups (By default
                        each group is adjusted independently)
  -a {none,fdr,bonferroni,BY,holm,hochberg,hommel}, --adjustment {none,fdr,bonferroni,BY,holm,hochberg,hommel}
                        p-value adjustment method (default='fdr')
  --csv                 Store results in output file in csv format (default)
  --json                Store results in output file in json format (default
                        is csv)

mutually exclusive required arguments:
  either a set or file must be provided

  -m MIRNA_SET [MIRNA_SET ...], --mirna-set MIRNA_SET [MIRNA_SET ...]
                        miRNA/precursor target set
  -M MIRNA_SET_FILE, --mirna-set-file MIRNA_SET_FILE
                        Specify miRNA/precursor target set via file

mutually exclusive optional arguments:
  either a set or file may be provided

  -c CATEGORIES [CATEGORIES ...], --categories CATEGORIES [CATEGORIES ...]
                        Set of categories to include in analysis, can include
                        `all`, `default`, `expert` or specific categories
  -C CATEGORIES_FILE, --categories-file CATEGORIES_FILE
                        File specifying categories to include in analysis

mutually exclusive optional arguments:
  either a set or file may be provided

  -r REFERENCE_SET [REFERENCE_SET ...], --reference-set REFERENCE_SET [REFERENCE_SET ...]
                        (Optional) Set of background miRNAs/precursors
  -R REFERENCE_SET_FILE, --reference-set-file REFERENCE_SET_FILE
                        (Optional) File specifying background
                        miRNAs/precursors
```

Examples:

```
$ mieaa ora hsa --precursors -M precursors.txt -C categories.txt > results.csv
$ mieaa ora hsa -p -M precursors.txt -c HMDD MNDR -o results.csv
$ mieaa ora hsa -p -M precursors.txt -C categories.txt -R reference.txt
$ mieaa ora mmu -M mirnas.txt -C categories.txt --adjustment none
$ mieaa ora rno -M mirnas.txt -C categories.txt -a bonferroni --json -o results.json
```


### open

Open the specified mieaa web tool page in browser

```
usage: miEAA open [-h] [-v] [-j JOB_ID] {input,progress,results}

positional arguments:
  {input,progress,results}
                        Open MiEAA interface in browser

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Always print results to stdout
  -j JOB_ID, --jobid JOB_ID
                        Job ID
```

Examples:

```
$ mieaa open input
$ mieaa open progress -j 31b41542-7856-40be-91b2-fd6afe28fa0b
$ mieaa open results --jobid 31b41542-7856-40be-91b2-fd6afe28fa0b
```
