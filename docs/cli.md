# Command Line Interface

Commands can be invoked via the command line using `mieaa SUBCOMMAND`.  
Help and options for all subcommands can be view with `mieaa SUBCOMMAND -h`

*Commands may require specifying whether the input is from a list of strings or a file (see `-m/M in Mutually exclusive options, below`).  
In such cases, the the lowercase flag letter specifies a string/list, and uppercase specifies a file.*

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
Each subcommand requires either `--mirna-set` (`-m`) or `--mirna-set-file` (`-M`) to be specified.
Enrichment analyses also require similarly behaving arguments for categories (`-c` or `-C`), and optionally for reference sets (`-r` or `-R`) in the case of ORA.

* `mieaa SUBCOMMAND --mirna-set MIRNA [MIRNA ...]`
* `mieaa SUBCOMMAND --mirna-set MIRNAS_STRING`
* `mieaa SUBCOMMAND --mirna-set-file MIRNA_FILE`

## Subcommands

### to_precursor

Convert miRNA -> precursor

* `mieaa to_precursor [-m | -M] [OPTIONS]`

```
$ mieaa to_precursor -m hsa-miR-20b-5p hsa-miR-144-5p --tabsep --unique
$ mieaa to_precursor -m 'hsa-miR-20b-5p,hsa-miR-144-5p' --newline -o precursors.txt
$ mieaa to_precursor -M mirnas.txt --outfile precursors.txt
```

### precursor_to_mirna

Converting between precursor -> miRNA

* `mieaa precursor_to_mirna [-m | -M] [OPTIONS]`

```
$ mieaa precursor_to_mirna -m hsa-mir-20b hsa-mir-144 --tabsep --unique
$ mieaa precursor_to_mirna -m 'hsa-mir-20b,hsa-mir-144' --newline -o mirnas.txt
$ mieaa precursor_to_mirna -M precursors.txt --outfile mirnas.txt
```

### convert_mirbase

Converting miRBase version

* `mieaa convert_mirbase FROM_VERSION [-m | -M] [OPTIONS]`

```
$ mieaa convert_mirbase 16 -m hsa-miR-642b,hsa-miR-550b
$ mieaa convert_mirbase 16 --to 22 -m hsa-miR-642b hsa-miR-550b
$ mieaa convert_mirbase 16  -M version_16.txt -o version_22.txt
```

### gsea

Gene Set Enrichment Analysis (GSEA)

* `mieaa gsea SPECIES [-m | -M] [-c | -C] [OPTIONS]`

Species must be specified using their three letter identifier, e.g. `hsa`, `mmu`, `rno`
The category flags (`-c -C`) behave identically to the miRNA set flags (`-m -M`).

```
$ mieaa gsea hsa --precursors -M precursors.txt -C categories.txt -o results.csv
$ mieaa gsea hsa -p -M precursors.txt -c HMDD MNDR > results.csv
$ mieaa gsea mmu -M mirnas.txt -C categories.txt --adjustment none
$ mieaa gsea rno -M mirnas.txt -C categories.txt -a bonferonni --json -o results.json
```

### ora

Over-representation Analysis (ORA)

* `mieaa ora SPECIES [-m | -M] [-c | -C] [OPTIONS]`

Species must be specified using their three letter identifier, e.g. `hsa`, `mmu`, `rno`.
The category flags (`-c -C`)  and reference set flags (`-r -R`) behave identically to the miRNA set flags (`-m -M`).

```
$ mieaa ora hsa --precursors -M precursors.txt -C categories.txt > results.csv
$ mieaa ora hsa -p -M precursors.txt -c HMDD MNDR -o results.csv
$ mieaa ora hsa -p -M precursors.txt -C categories.txt -R reference.txt
$ mieaa ora mmu -M mirnas.txt -C categories.txt --adjustment none
$ mieaa ora rno -M mirnas.txt -C categories.txt -a bonferonni --json -o results.json
```
