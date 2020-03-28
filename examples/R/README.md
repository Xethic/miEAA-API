# miEAA API Usage
The [reticulate](https://github.com/rstudio/reticulate) library allows us to utilize the wrapper class in R, assuming Python is also installed.

A barebones example script can be found [here](./example_script.R).

```R
library(reticulate)
mieaa = import("mieaa")
mieaa_api = mieaa$API()
```

Target sets, categories, and reference sets support strings, iterables, and file objects.

Mixed delimiters should still function, but are not recommended.


```R
# list('hsa-miR-374c', 'hsa-miR-642b', 'hsa-miR-550b', 'hsa-miR-107', 'hsa-miR-125b')
initial_mirnas = 'hsa-miR-374c hsa-miR-642b,hsa-miR-550b;hsa-miR-107;hsa-miR-125b'
```

## Convert between miRBase versions
Results can be optionally saved to a file by specifying the `to_file` argument.


```R
# mieaa_api$convert_mirbase_version(initial_precursors, '9.1', '22', 'precursor', to_file='mirnas.txt')
updated_mirnas = mieaa_api$convert_mirbase_version(initial_mirnas, '16', '22', 'mirna')
updated_mirnas
```

```R
[[1]]
[1] "hsa-miR-374c-5p"

[[2]]
[1] "hsa-miR-642b-3p"

[[3]]
[1] "hsa-miR-550b-3p"

[[4]]
[1] "hsa-miR-107"

[[5]]
[1] "hsa-miR-125b-5p"
```

## Convert between miRNAs <-> precursors
Results can be optionally saved to a file by specifying the `to_file` argument.    
Some names are not uniquely converted. We can specify conversion type as either `all` (default) or `unique`.  
We can also decide whether we want our output to only include converted results with multiple-mapped values separated by a semicolon (default, `oneline`), 
on their own individual lines (`newline`), or a tab separated input - output (`tabsep`).


```R
precursors = mieaa_api$convert_mirna_to_precursor(updated_mirnas, to_file='./precursors.txt', conversion_type='all')
precursors
```



```R
[[1]]
[1] "hsa-mir-374c"

[[2]]
[1] "hsa-mir-642b"

[[3]]
[1] "hsa-mir-550b-1;hsa-mir-550b-2"

[[4]]
[1] "hsa-mir-107"

[[5]]
[1] "hsa-mir-125b-1;hsa-mir-125b-2"
```



```R
py = import_builtins()  # part of 'reticulate'

# Files need to be python file objects
with(py$open("precursors.txt", 'r') %as% prec_file, {
    mirnas = mieaa_api$convert_precursor_to_mirna(prec_file, output_format='tabsep')
})
mirnas
```


```R
[[1]]
[1] "hsa-mir-374c\thsa-miR-374c-5p;hsa-miR-374c-3p"

[[2]]
[1] "hsa-mir-642b\thsa-miR-642b-5p;hsa-miR-642b-3p"

[[3]]
[1] "hsa-mir-550b-1\thsa-miR-550b-3p;hsa-miR-550b-2-5p"

[[4]]
[1] "hsa-mir-550b-2\thsa-miR-550b-3p;hsa-miR-550b-2-5p"

[[5]]
[1] "hsa-mir-107\thsa-miR-107"

[[6]]
[1] "hsa-mir-125b-1\thsa-miR-125b-5p;hsa-miR-125b-1-3p"

[[7]]
[1] "hsa-mir-125b-2\thsa-miR-125b-5p;hsa-miR-125b-2-3p"
```

## Enrichment Analysis

### Starting Enrichment Analysis
Run Gene Set Enrichment Analysis (GSEA) or Over-representation Analysis (ORA).  
Please refer to documentation for possible keyword arguments.

For ORA, if `reference_set` is not specified or is left empty, default to using miEAA reference sets for specified categories.


```R
# mieaa_api$run_gsea(precursors, ['HMDD, mndr'], 'precursor', 'hsa')
with(py$open("precursors.txt", 'r') %as% test_set_file, {
    mieaa_api$run_ora(test_set_file, list('HMDD, mndr'), 'precursor', 'hsa', reference_set='')
})
```


#### Viewing computation progress


```R
mieaa_api$get_progress()
```


0.7


### Retrieving Enrichment Results
Get results after enrichment analysis has been completed, determining how often to check progress via `check_progress_interval` (default is 5 seconds).


```R
json = mieaa_api$get_results(check_progress_interval=5)
```

The returned data can be easily turned into a dataframe.


```R
cols = c('category', 'subcategory', 'enrichment', 'p-value', 'p-adjusted', 'q-value', 'expected', 'observed', 'mirnas/precursors')
df = data.frame(matrix(unlist(json), nrow=length(json), byrow=T))
colnames(df) = cols
head(df)
```


<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>category</th>
      <th>subcategory</th>
      <th>enrichment</th>
      <th>p-value</th>
      <th>p-adjusted</th>
      <th>q-value</th>
      <th>expected</th>
      <th>observed</th>
      <th>mirnas/precursors</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Diseases (HMDD)</td>
      <td>Alopecia</td>
      <td>over-represented</td>
      <td>0.0017138</td>
      <td>0.0478121</td>
      <td>0.0478121</td>
      <td>0.0678879</td>
      <td>2</td>
      <td>hsa-mir-125b-1; hsa-mir-125b-2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Diseases (HMDD)</td>
      <td>Atopic Dermatitis</td>
      <td>over-represented</td>
      <td>0.0021345</td>
      <td>0.0478121</td>
      <td>0.0478121</td>
      <td>0.075431</td>
      <td>2</td>
      <td>hsa-mir-125b-1; hsa-mir-125b-2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Diseases (HMDD)</td>
      <td>Lichen Planus</td>
      <td>over-represented</td>
      <td>0.0017138</td>
      <td>0.0478121</td>
      <td>0.0478121</td>
      <td>0.0678879</td>
      <td>2</td>
      <td>hsa-mir-125b-1; hsa-mir-125b-2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Diseases (HMDD)</td>
      <td>Myotonic Muscular Dystrophy</td>
      <td>over-represented</td>
      <td>6.36e-4</td>
      <td>0.0356009</td>
      <td>0.0356009</td>
      <td>0.196121</td>
      <td>3</td>
      <td>hsa-mir-107; hsa-mir-125b-1; hsa-mir-125b-2</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Diseases (HMDD)</td>
      <td>Nevus</td>
      <td>over-represented</td>
      <td>1.46e-4</td>
      <td>0.0163454</td>
      <td>0.0163454</td>
      <td>0.0226293</td>
      <td>2</td>
      <td>hsa-mir-125b-1; hsa-mir-125b-2</td>
    </tr>
  </tbody>
</table>



Results can also be obtained as a csv string.


```R
csv_string = mieaa_api$get_results('csv')
```

### Saving Enrichment Results
Results can be automatically saved to a json or csv (default) file. 


```R
# mieaa_api$save_enrichment_results('./example.json', file_type='json')
file_contents = mieaa_api$save_enrichment_results('./results.csv')
```

Alternatively, we can write the csv results to a file.


```R
outfile = file("./results_2.csv")
writeLines(csv_string, outfile)
close(outfile)
```

## Miscellaneous
After running an analysis, we may wish to view the parameters we used for our analysis.  


```R
mieaa_api$get_enrichment_parameters()
```


    $enrichment_analysis
    [1] "ORA"
    
    $p_value_adjustment
    [1] "fdr"
    
    $independent_p_adjust
    [1] TRUE
    
    $significance_level
    [1] 0.05
    
    $threshold_level
    [1] 2
    
    $categories
    [1] "HMDD_precursor" "MNDR_precursor"
    
    $reference_set
    [1] ""
    
    $testset_file
    <_io.TextIOWrapper name='precursors.txt' mode='r' encoding='UTF-8'>



Upon running an analysis, our API instance is assigned a unique Job ID.  
If we wish to reuse the same instance to run a new analysis, we must first invalidate it, making our current results irretrievable.


```R
mieaa_api$invalidate()
```
