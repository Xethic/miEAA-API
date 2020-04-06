import requests
from http.client import RemoteDisconnected
from io import IOBase
from re import findall
from time import sleep, time
from typing import List, IO, Iterable, Union


def descriptive_http_error(response):
    try:
        response.raise_for_status()
    except requests.HTTPError as err:
        raise requests.HTTPError('{}\nResponse: {}'.format(err, response.text))


class API_Session(requests.Session):
    """ Extend requests.Session to allow waiting a specified number of sessions between requests """
    def __init__(self, *args, **kwargs):
        super(API_Session, self).__init__(*args, **kwargs)
        self.last_request = time()

    def wait_request(self, *args, wait=1, **kwargs):
        """ Wait specified number of seconds between requests """
        elapsed = time() - self.last_request
        wait += .1  # wait just a tad bit longer to allow time to send request
        if elapsed < wait:
            sleep(wait - elapsed)
        request = self.request(*args, **kwargs)
        self.last_request = time()
        return request

    def wait_post(self, *args, **kwargs):
        return self.wait_request('POST', *args, **kwargs)

    def wait_get(self, *args, **kwargs):
        return self.wait_request('GET', *args, **kwargs)


class API:
    """ miEAA api wrapper class.
    Each instance is tied to a Job ID after starting an enrichment analysis.
    Instance must be invalidated with `invalidate()` before starting a new analysis.

    Attributes
    ----------
    root_url [class attribute] : str
        API root url
    api_version [class attribute] : str
        Current API version
    endpoints [class attribute] : dict
        API endpoints suffix
    wait_between_requests [class attribute] : float
        How many seconds to wait between API requests (due to throttling)
    default [class attribute] : dict
        Default settings to pass to converter or analysis apis
    session [instance attribute] : API_Session
        Session information necessary to retrieve results
    job_id [instance attribute] : uuid
        Unique identifier for enrichment analysis job of current session
    """

    root_url = "https://anathema.cs.uni-saarland.de/mieaa_tool/api/"
    api_version = 'v1'
    wait_between_requests = 1

    endpoints = {
        'categories': 'enrichment_categories/{species}/{mirna}/',
        'mirbase_converter': 'mirbase_converter/',
        'mirna_type_converter': 'mirna_precursor_converter/',
        'enrichment': 'enrichment_analysis/{species}/{mirna}/{analysis}/',
        'results': 'enrichment_analysis/results/{job_id}/',
        'status': 'job_status/{job_id}/',
    }

    default_params = {
        'converter': {
            'output_format': 'oneline',
            'conversion_type': 'all',
        },
        'analysis': {
            'p_value_adjustment': 'fdr',
            'independent_p_adjust': True,
            'significance_level': 0.05,
            'threshold_level': 2,
        }
    }

    def __init__(self):
        self.session = API_Session()
        self.job_id = None
        self._enrichment_parameters = None
        self._cached_results_type = None
        self.results_response = None

    def invalidate(self):
        """ Invalidate current session. Results will become irretrievable."""
        self.session.close()
        self.job_id = None
        self._enrichment_parameters = None
        self._cached_results_type = None
        self.results_response = None

    def convert_mirbase(self, mirnas: Union[str, Iterable[str], IO], from_version: float, to_version: float,
                                mirna_type: str, to_file: Union[str, IO]='', **kwargs) -> List[str]:
        """ Convert a set of either miRNAs/precursors from one miRbase version to another

        Parameters
        -----------
        mirnas : str or iterable
            Iterable or delimited string of miRNAs, e.g. 'hsa-miR-199a-5p,hsa-mir-550b-1;'
        from_version : float
            MiRbase version to convert 'mirnas' from.
        to_version : float
            MiRbase version to update 'mirnas' to.
        mirna_type : str
            miRNAs/precursors to convert
            * *precursor* - Precursor to a mature miRNA, e.g. hsa-mir-550b-1
            * *mirna* - Mature miRNA, e.g. hsa-miR-199a-5p
            Mixed input is not currently supported.
        to_file : str or file-type, optional
            if non-empty, save results to provided file name/path
        **kwargs
            output_format (str, default='oneline')
                * *oneline* - Text containing only converted ids
                * *tabsep* - Tab-separated input and output id

        Returns
        -------
        list
            Converted miRNAs
        """
        if isinstance(mirnas, IOBase):
            mirnas = mirnas.read().splitlines()
        if not isinstance(mirnas, str):
            mirnas = ';'.join(mirnas)
        base_payload = {
            'mirnas': mirnas,
            'input_type': mirna_type.lower(),
            'mirbase_input_version': 'v{}'.format(from_version),
            'mirbase_output_version': 'v{}'.format(to_version),
        }

        return self._convert('mirbase_converter', base_payload, to_file, kwargs)

    def _convert_mirna_type(self, mirnas: Union[str, Iterable[str], IO], conversion: str,
                           to_file: Union[str, IO]='', **kwargs) -> List[str]:
        """ Convert from precursor->mirna or mirna-> precursor

        Parameters
        -----------
        mirnas : str or iterable
            Iterable or delimited string of miRNAs, e.g. 'hsa-miR-199a-5p,hsa-mir-550b-1'
        conversion : str
            * *to_mirna* - Convert precursors to miRNAs
            * *to_precursor* - Convert mirna to precursors
        to_file : str, optional
            if non-empty, save results to provided file name/path
        **kwargs
            output_format (str, default='oneline')
                * *oneline* - Text containing only converted ids, multi-mapped are semicolon separated
                * *newline* - Text containing only converted ids, multi-mapped are newline separated
                * *tabsep* - Tab-separated input and output id
            conversion_type (str, default='all')
                * *all* - Output all mappings
                * *unique* - Only output unique mappings

        Returns
        -------
        list
            Converted miRNAs
        """
        if isinstance(mirnas, IOBase):
            mirnas = mirnas.read().splitlines()
        if not isinstance(mirnas, str):
            mirnas = ';'.join(mirnas)
        base_payload = {
            'mirnas': mirnas,
            'input_type': conversion.lower()
        }

        return self._convert('mirna_type_converter', base_payload, to_file, kwargs)

    def to_mirna(self, mirnas: Union[str, Iterable[str], IO],
                                   to_file: Union[str, IO]='', **kwargs) -> List[str]:
        """ Convert from precursor->mirna

        Parameters
        -----------
        mirnas : str or iterable
            Iterable or delimited string of miRNAs, e.g. 'hsa-miR-199a-5p,hsa-mir-550b-1'
        to_file : str, optional
            if non-empty, save results to provided file name/path
        **kwargs
            output_format (str, default='oneline')
                * *oneline* - Text containing only converted ids, multi-mapped are semicolon separated
                * *newline* - Text containing only converted ids, multi-mapped are newline separated
                * *tabsep* - Tab-separated input and output id
            conversion_type (str, default='all')
                * *all* - Output all mappings
                * *unique* - Only output unique mappings

        Returns
        -------
        list
            Converted miRNAs
        """
        return self._convert_mirna_type(mirnas, 'to_mirna', to_file, **kwargs)

    def to_precursor(self, mirnas: Union[str, Iterable[str], IO],
                                   to_file: Union[str, IO]='', **kwargs) -> List[str]:
        """ Convert from mirna->precursor

        Parameters
        -----------
        mirnas : str or iterable
            Iterable or delimited string of miRNAs, e.g. 'hsa-miR-199a-5p,hsa-mir-550b-1'
        to_file : str, optional
            if non-empty, save results to provided file name/path
        **kwargs
            output_format (str, default='oneline')
                * *oneline* - Text containing only converted ids, multi-mapped are semicolon separated
                * *newline* - Text containing only converted ids, multi-mapped are newline separated
                * *tabsep* - Tab-separated input and output id
            conversion_type (str, default='all')
                * *all* - Output all mappings
                * *unique* - Only output unique mappings

        Returns
        -------
        list
            Converted miRNAs
        """
        return self._convert_mirna_type(mirnas, 'to_precursor', to_file, **kwargs)

    def _start_analysis(self, analysis_type: str, test_set: Union[str, Iterable, IO],
                       categories: Union[str, Iterable, IOBase], mirna_type: str, species: str,
                       reference_set: Union[str, Iterable, IOBase]='', **kwargs) -> requests.Response:
        """ Start Enrichment Analysis

        Parameters
        -----------
        analysis_type : str
            * *ORA* - Over-representation Analysis
            * *GSEA* - miRNA enrichment analysis
        test_set : str, iterable or file-like
            set of miRNAs/precursors we want to test
        categories : str, iterable or file-like
            Categories we want to run analysis on
        mirna_type : str
            * *precursor* - Precursor to a mature miRNA, e.g. hsa-mir-550b-1
            * *mirna* - Mature miRNA, e.g. hsa-miR-199a-5p
        species : str
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
        reference_set : str or file-like, default=''
            ORA specific, background reference set of miRNAs/precursors

        **kwargs
            p_value_adjustment (str, default='fdr')
                * *none* - No adjustment
                * *fdr* - FDR (Benjamini-Hochberg) adjustment
                * *bonferroni* - Bonferroni adjustment
                * *BY* - Benjamini-Yekutieli adjustment
                * *hochberg* - Hochberg adjustment
                * *holm* - Holm adjustment
                * *hommel* - Hommel adjustment
            independent_p_adjust (bool, default=True)
                * *True* - Adjust p-values for each category independently
                * *False* - Adjust p-values for all categories collectively
            significance_level (float, default=0.05)
                Filter out p-values above significance level
            threshold_level (int, default=2)
                Filter out subcategories that contain less than this many miRNAs

        Returns
        -------
        requests.Response
            Response
        """
        def format_categories(categories, mirna_type, species):
            categories = findall(r'\b\w+\b', categories)
            suffix = '_precursor' if mirna_type == 'precursor' else '_mature'
            # map lowercase names to category name
            cased = {key.lower() + suffix: key + suffix for key in self.get_enrichment_categories(mirna_type, species)}
            # add suffix to provided categories
            categories = [cat if cat.endswith(suffix) else cat + suffix for cat in categories]
            return [cased.get(cat.lower(), cat) for cat in categories]

        if self.job_id:
            raise RuntimeError("You must call `invalidate()` method before starting a new analysis. This will cause you to lose access to current analysis")

        # check if categories is a file or iterable
        if isinstance(categories, IOBase):
            categories = categories.read()
        else:
            categories = categories if isinstance(categories, str) else ';'.join(categories)

        base_payload = {
            'categories': format_categories(categories, mirna_type, species)
        }
        files = {}

        payload = self._extend_payload(base_payload, kwargs, 'analysis')

        # check if test set is file or string
        if isinstance(test_set, IOBase):
            files['testset_file'] = test_set
        else:
            payload['testset'] = test_set if isinstance(test_set, str) else ';'.join(test_set)

        # check if reference set is file or string
        if isinstance(reference_set, IOBase):
            files['reference_set_file'] = reference_set
            payload['reference_set'] = ''
        else:
            payload['reference_set'] = reference_set if isinstance(reference_set, str) else ';'.join(reference_set)

        url = self._get_endpoint('enrichment', species=species.lower(),
                                 analysis=analysis_type.upper(), mirna=mirna_type.lower())

        response = self.session.wait_post(url, data=payload, files=files, wait=self.wait_between_requests)
        descriptive_http_error(response)

        try:
            self.job_id = response.json()['job_id']
        except Exception as err:
            print(err)
            print(response.text)
            return response

        self._enrichment_parameters = {'enrichment_analysis': analysis_type, **payload, **files}

        return response

    def run_ora(self, test_set: Union[str, Iterable, IO], categories: Iterable, mirna_type: str,
                species: str, reference_set: Union[str, IOBase]='', **kwargs):
        """ Start Over Enrichment Analysis

        Parameters
        -----------
        test_set : str, iterable or file-like
            set of miRNAs/precursors we want to test
        categories : str, iterable or file-like
            Categories we want to run analysis on
        mirna_type : str
            * *precursor* - Precursor to a mature miRNA, e.g. hsa-mir-550b-1
            * *mirna* - Mature miRNA, e.g. hsa-miR-199a-5p
        species : str
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
        reference_set : str or file-like, default=''
            ORA specific, background reference set of miRNAs/precursors

        **kwargs
            p_value_adjustment (str, default='fdr')
                * *none* - No adjustment
                * *fdr* - FDR (Benjamini-Hochberg) adjustment
                * *bonferroni* - Bonferroni adjustment
                * *BY* - Benjamini-Yekutieli adjustment
                * *hochberg* - Hochberg adjustment
                * *holm* - Holm adjustment
                * *hommel* - Hommel adjustment
            independent_p_adjust (bool, default=True)
                * *True* - Adjust p-values for each category independently
                * *False* - Adjust p-values for all categories collectively
            significance_level (float, default=0.05)
                Filter out p-values above significance level
            threshold_level (int, default=2)
                Filter out subcategories that contain less than this many miRNAs

        Returns
        -------
        requests.Response
            Response
        """
        return self._start_analysis('ORA', test_set, categories, mirna_type, species, reference_set, **kwargs)

    def run_gsea(self, test_set: Union[str, Iterable, IO], categories: Iterable, mirna_type: str,
                 species: str, **kwargs):
        """ Start miRNA Set Enrichment Analysis

        Parameters
        -----------
        test_set : str, iterable or file-like
            set of miRNAs/precursors we want to test
        categories : str, iterable or file-like
            Categories we want to run analysis on
        mirna_type : str
            * *precursor* - Precursor to a mature miRNA, e.g. hsa-mir-550b-1
            * *mirna* - Mature miRNA, e.g. hsa-miR-199a-5p
        species : str
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
        reference_set : str or file-like, default=''
            ORA specific, background reference set of miRNAs/precursors

        **kwargs
            p_value_adjustment (str, default='fdr')
                * *none* - No adjustment
                * *fdr* - FDR (Benjamini-Hochberg) adjustment
                * *bonferroni* - Bonferroni adjustment
                * *BY* - Benjamini-Yekutieli adjustment
                * *hochberg* - Hochberg adjustment
                * *holm* - Holm adjustment
                * *hommel* - Hommel adjustment
            independent_p_adjust (bool, default=True)
                * *True* - Adjust p-values for each category independently
                * *False* - Adjust p-values for all categories collectively
            significance_level (float, default=0.05)
                Filter out p-values above significance level
            threshold_level (int, default=2)
                Filter out subcategories that contain less than this many miRNAs

        Returns
        -------
        requests.Response
            Response
        """
        return self._start_analysis('GSEA',  test_set, categories, mirna_type, species, '', **kwargs)

    def _get_progress_response(self):
        if not self.job_id:
            raise RuntimeError('No enrichment analysis has been initiated.')
        url = self._get_endpoint('status', job_id=self.job_id)
        response = self.session.wait_get(url, wait=self.wait_between_requests)
        descriptive_http_error(response)
        return response

    def get_progress(self):
        """ Retrieve enrichment analysis progress """
        return self._get_progress_response().json()['status']

    def get_results(self, results_format: str='json', check_progress_interval: float=5., retries=5) -> Union[str, list]:
        """ Return results in json or csv format

        Parameters
        -----------
        results_format: str, default='json'
            * *json* - retrieve results in json format
            * *csv* - retrieve results in csv format
        check_progress_interval: float
            How many seconds to wait between checking if results have been computed

        Returns
        -------
        requests.Response
            Response
        """
        if not self.job_id:
            raise RuntimeError('No enrichment analysis has been initiaited.')

        if self._cached_results_type == results_format and self.results_response is not None:
            if results_format == 'json':
                return self.results_response.json()
            return self.results_response.text

        self._cached_results_type = results_format
        progress = 0

        for _ in range(retries):
            try:
                while progress < 100:
                    sleep(check_progress_interval)
                    progress = self.get_progress()
                    if progress == 'FAILED':
                        return [] if results_format == 'json' else ''

                url = self._get_endpoint('results', job_id=self.job_id)
                response = self.session.wait_get(url, params={'format': results_format}, wait=self.wait_between_requests)
                descriptive_http_error(response)
                self.results_response = response
                if results_format == 'json':
                    return self.results_response.json()
                return self.results_response.text
            except requests.exceptions.ConnectionError as e:
                pass

    def get_enrichment_categories(self, mirna_type: str, species: str, with_suffix=False) -> dict:
        """ Get possible enrichment categories

        Parameters
        -----------
        mirna_type : str
            * *precursor* - Precursor to a mature miRNA, e.g. hsa-mir-550b-1
            * *mirna* - Mature miRNA, e.g. hsa-miR-199a-5p
        species : str
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
        with_suffix : bool, default=False
            whether to include '_precursor' or '_mature' at end of category name

        Returns
        -------
        dict
            Keys are categories and values are their descriptions
        """
        url = self._get_endpoint('categories', species=species.lower(), mirna=mirna_type.lower())
        response = self.session.wait_get(url, wait=self.wait_between_requests)
        descriptive_http_error(response)
        categories = response.json()['categories']

        if with_suffix:
            return {cat: desc for cat, desc in categories}

        cat_suffix = '_precursor' if mirna_type == 'precursor' else '_mature'
        return {cat.replace(cat_suffix, ''): desc for cat, desc in categories}

    def save_enrichment_results(self, save_file: Union[str, IO], file_type: str='csv',
                                check_progress_interval: float=5.) -> str:
        """ Save results in specified format

        Parameters
        ----------
        save_file : str or file-like
            File to save results in
        file_type : str, default='csv'
            Type of file to write results to. Options are `json` or `csv`
        check_progress_interval : float, default=5
            How many seconds to wait between checking if results have been computed
        """
        results = str(self.get_results(file_type, check_progress_interval))
        if isinstance(save_file, IOBase):
            save_file.write(results)
        else:
            with open(save_file, 'w+') as outfile:
                outfile.write(results)
        return results

    def get_enrichment_parameters(self):
        """ Retrieve parameters used during enrichment analysis"""
        if not self.job_id:
            raise RuntimeError('No enrichment analysis has been initiated.')
        return self._enrichment_parameters

    def _convert(self, converter_type, base_payload, to_file, default_overrides):
        """fill in defaults and return converted mirnas"""
        url = self._get_endpoint(converter_type)
        payload = self._extend_payload(base_payload, default_overrides, 'converter')

        response = self.session.wait_post(url, data=payload, wait=self.wait_between_requests)
        descriptive_http_error(response)

        if isinstance(to_file, IOBase):
            to_file.write(response.text)
            to_file.close()
        elif to_file:
            with open(to_file, 'w+') as savefile:
                savefile.write(response.text)

        return response.text.splitlines()

    def _extend_payload(self, payload: dict, default_overrides: dict, default_name: str=''):
        """ Fill in default payload, overriding as provided """
        defaults = self.default_params[default_name] if default_name else {}
        return {
            **defaults,
            **default_overrides,
            **payload
        }

    def _get_endpoint(self, endpoint: str, **kwargs) -> str:
        base_url = '{}{}/'.format(self.root_url, self.api_version)
        endpoint = self.endpoints[endpoint].format(**kwargs)
        return requests.compat.urljoin(base_url, endpoint)
