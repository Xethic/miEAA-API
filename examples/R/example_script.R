library(reticulate)
py = import_builtins()
mieaa = import("mieaa")
mieaa_api = mieaa$API()

initial_mirnas = 'hsa-miR-374c hsa-miR-642b,hsa-miR-550b;hsa-miR-107;hsa-miR-125b'

updated_mirnas = mieaa_api$convert_mirbase(initial_mirnas, '16', '22', 'mirna')

precursors = mieaa_api$to_precursor(updated_mirnas, to_file='./precursors.txt', conversion_type='all')

with(py$open("precursors.txt", 'r') %as% test_set_file, {
    mieaa_api$run_ora(test_set_file, list('HMDD, mndr'), 'precursor', 'hsa', reference_set='')
})

print(mieaa_api$get_progress())

json = mieaa_api$get_results(check_progress_interval=5)

cols = c('category', 'subcategory', 'enrichment', 'p-value', 'p-adjusted', 'q-value', 'expected', 'observed', 'mirnas/precursors')
df = data.frame(matrix(unlist(json), nrow=length(json), byrow=T))
colnames(df) = cols

mieaa_api$save_enrichment_results('./results.csv')

print(mieaa_api$get_enrichment_parameters())

mieaa_api$new_session()
