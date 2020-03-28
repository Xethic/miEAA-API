# miEAA API Wrapper Usage

A barebones example script can be found [here](./example_script.py).

```python
from mieaa import API

mieaa_api = API()
```

Target sets, categories, and reference sets support strings, iterables, and file objects.

Mixed delimiters should still function, but are not recommended.


```python
#initial_mirnas = ['hsa-miR-374c', 'hsa-miR-642b', 'hsa-miR-550b', 'hsa-miR-107', 'hsa-miR-125b']
initial_mirnas = 'hsa-miR-374c hsa-miR-642b,hsa-miR-550b;hsa-miR-107;hsa-miR-125b'
```

## Convert between miRBase versions
Results can be optionally saved to a file by specifying the `to_file` argument.


```python
# mieaa_api.convert_mirbase_version(initial_precursors, 9.1, 22, 'precursor', to_file='mirnas.txt')
updated_mirnas = mieaa_api.convert_mirbase_version(initial_mirnas, 16, 22, 'mirna')
updated_mirnas
```




    ['hsa-miR-374c-5p',
     'hsa-miR-642b-3p',
     'hsa-miR-550b-3p',
     'hsa-miR-107',
     'hsa-miR-125b-5p']



## Convert between miRNAs <-> precursors
Results can be optionally saved to a file by specifying the `to_file` argument.    
Some names are not uniquely converted. We can specify conversion type as either `all` (default) or `unique`.  
We can also decide whether we want our output to only include converted results with multiple-mapped values separated by a semicolon (default, `oneline`), 
on their own individual lines (`newline`), or a tab separated input - output (`tabsep`).


```python
precursors = mieaa_api.convert_mirna_to_precursor(updated_mirnas, to_file='./precursors.txt', conversion_type='all')
precursors
```




    ['hsa-mir-374c',
     'hsa-mir-642b',
     'hsa-mir-550b-1;hsa-mir-550b-2',
     'hsa-mir-107',
     'hsa-mir-125b-1;hsa-mir-125b-2']




```python
with open('./precursors.txt') as prec_file:
    mirnas = mieaa_api.convert_precursor_to_mirna(prec_file, output_format='tabsep')
mirnas
```




    ['hsa-mir-374c\thsa-miR-374c-5p;hsa-miR-374c-3p',
     'hsa-mir-642b\thsa-miR-642b-5p;hsa-miR-642b-3p',
     'hsa-mir-550b-1\thsa-miR-550b-3p;hsa-miR-550b-2-5p',
     'hsa-mir-550b-2\thsa-miR-550b-3p;hsa-miR-550b-2-5p',
     'hsa-mir-107\thsa-miR-107',
     'hsa-mir-125b-1\thsa-miR-125b-5p;hsa-miR-125b-1-3p',
     'hsa-mir-125b-2\thsa-miR-125b-5p;hsa-miR-125b-2-3p']



## Enrichment Analysis

### Starting Enrichment Analysis
Run Gene Set Enrichment Analysis (GSEA) or Over-representation Analysis (ORA).  
Please refer to documentation for possible keyword arguments.

For ORA, if `reference_set` is not specified or is left empty, default to using miEAA reference sets for specified categories. 


```python
# mieaa_api.run_gsea(precursors, ['HMDD, mndr'], 'precursor', 'hsa')
with open('./precursors.txt', 'r') as test_set_file:
    mieaa_api.run_ora(test_set_file, ['HMDD, mndr'], 'precursor', 'hsa', reference_set='')
```

#### Viewing computation progress


```python
mieaa_api.get_progress()
```




    0.7



### Retrieving Enrichment Results
Get results after enrichment analysis has been completed, determining how often to check progress via `check_progress_interval` (default is 5 seconds).


```python
json = mieaa_api.get_results(check_progress_interval=5)
```

The returned data can be easily turned into a pandas dataframe.


```python
import pandas as pd 
cols = ['category', 'subcategory', 'enrichment', 'p-value', 'q-value', 'expected', 'observed', 'mirnas/precursors']
df = pd.DataFrame(json, columns=cols)
df.head()
```




<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>category</th>
      <th>subcategory</th>
      <th>enrichment</th>
      <th>p-value</th>
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
      <td>0.047812127999999995</td>
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
      <td>0.047812127999999995</td>
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
      <td>0.047812127999999995</td>
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
      <td>0.03560088</td>
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
      <td>0.016345392</td>
      <td>0.0163454</td>
      <td>0.0226293</td>
      <td>2</td>
      <td>hsa-mir-125b-1; hsa-mir-125b-2</td>
    </tr>
  </tbody>
</table>




Results can also be obtained as a csv string.


```python
csv_string = mieaa_api.get_results('csv')
```

### Saving Enrichment Results
Results can be automatically saved to a json or csv (default) file. 


```python
# mieaa_api.save_enrichment_results('./example.json', file_type='json')
file_contents = mieaa_api.save_enrichment_results('./results.csv')
```

Alternatively, we can write the csv results to a file.


```python
with open('results_2.csv', 'w+') as outfile:
    outfile.write(csv_string)
```

## Miscellaneous
After running an analysis, we may wish to view the parameters we used for our analysis.  


```python
mieaa_api.get_enrichment_parameters()
```




    {'enrichment_analysis': 'ORA',
     'p_value_adjustment': 'fdr',
     'independent_p_adjust': True,
     'significance_level': 0.05,
     'threshold_level': 2,
     'categories': ['HMDD_precursor', 'MNDR_precursor'],
     'reference_set': '',
     'testset_file': <_io.TextIOWrapper name='./precursors.txt' mode='r' encoding='UTF-8'>}



Upon running an analysis, our API instance is assigned a unique Job ID.  
If we wish to reuse the same instance to run a new analysis, we must first invalidate it, making our current results irretrievable.


```python
mieaa_api.invalidate()
```
