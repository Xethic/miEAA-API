# import pandas as pd
from mieaa import API

mieaa_api = API()

initial_mirnas = 'hsa-miR-374c hsa-miR-642b,hsa-miR-550b;hsa-miR-107;hsa-miR-125b'

updated_mirnas = mieaa_api.convert_mirbase_version(initial_mirnas, 16, 22, 'mirna')

precursors = mieaa_api.convert_mirna_to_precursor(updated_mirnas, to_file='./precursors.txt', conversion_type='all')


with open('./precursors.txt', 'r') as test_set_file:
    mieaa_api.run_ora(test_set_file, ['HMDD, mndr'], 'precursor', 'hsa', reference_set='')

print(mieaa_api.get_progress())

json = mieaa_api.get_results(check_progress_interval=5)

mieaa_api.save_enrichment_results('./example.csv')

## Pandas required
# cols = ['category', 'subcategory', 'enrichment', 'p-value', 'q-value', 'expected', 'observed', 'mirnas/precursors']
# df = pd.DataFrame(json, columns=cols)
# df.head()

mieaa_api.save_enrichment_results('./results.csv')

print(mieaa_api.get_enrichment_parameters())

# mieaa_api.invalidate()
