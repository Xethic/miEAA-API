import argparse
from mieaa.mieaa_wrapper import API
from mieaa._version import __version__

def type_converter(mieaa, args):
    mirnas = args.mirna_set_file or args.mirna_set
    return mieaa._convert_mirna_type(mirnas, args.parser_name, args.outfile,
                                    conversion_type=args.conv_type, output_format=args.out_format)


def mirbase_converter(mieaa, args):
    mirnas = args.mirna_set_file or args.mirna_set
    formatting = 'oneline' if args.out_format == 'newline' else args.out_format
    return mieaa.convert_mirbase(mirnas, args.from_, args.to, args.mirna_type, args.outfile,
                                         output_format=args.out_format)


def enrichment_analsis(mieaa, args):
    mirnas = args.mirna_set_file or args.mirna_set
    categories = args.categories_file.read().splitlines() if args.categories_file else args.categories
    for option in ['all', 'default', 'defaults', 'expert']:
        if option in categories:
            categories.remove(option)
            categories.extend(mieaa.get_enrichment_categories(args.mirna_type, args.species, option))
    categories = set(categories)

    ref_set = ''
    if args.parser_name == 'ora':
        if args.reference_set_file:
            ref_set = args.reference_set_file.read().splitlines()
        elif args.reference_set:
            ref_set = args.reference_set

    mieaa._start_analysis(args.parser_name.upper(), mirnas, categories, args.mirna_type, args.species, ref_set,
                         p_value_adjustment=args.adjustment, independent_p_adjust=args.indep_adjust,
                         significance_level=args.significance, threshold_level=args.threshold)
    if args.verbose:
        print(f'Started analysis with Job ID: {mieaa.job_id}')

    if args.no_results:
        return mieaa.job_id
    if args.outfile:
        return mieaa.save_enrichment_results(args.outfile, args.outfile_type)
    return mieaa.get_results()


def open_browser(mieaa, args):
    return mieaa.open_gui(args.open, args.job_id)

def create_subcommands(subparsers):
    def mutex_help_text(required=True):  # title and description of help groups
        if required:
            return "mutually exclusive required arguments", "either a set or file must be provided"
        return "mutually exclusive optional arguments", "either a set or file may be provided"

    # Abstract Parsers
    # ----------------
    # Parent parser with requirements inherited by all subcommands
    base_parser = argparse.ArgumentParser(add_help=False)
    base_parser.add_argument('-v', '--verbose', action='store_true', help='Always print results to stdout')

    # Abstract parser for any commands involving mirnas
    mirna_parser = argparse.ArgumentParser(add_help=False, parents=[base_parser])
    mirna_set_group = mirna_parser.add_argument_group(*mutex_help_text(required=True))
    mirna_set_group.add_argument('-m', '--mirna-set', nargs='+', help='miRNA/precursor target set')
    mirna_set_group.add_argument('-M', '--mirna-set-file', type=argparse.FileType('r'),
        help='Specify miRNA/precursor target set via file')
    mirna_parser.add_argument('-p', '--precursor', '--precursors', action='store_const', const='precursor',
        default='mirna', dest='mirna_type', help='Use if running on a set of precursors as opposed to miRNAs')
    mirna_parser.add_argument('-o', '--outfile', type=argparse.FileType('w+'),
        help='Save results to provided file')

    # Abstract Converter applicable to all converters
    converter_parser = argparse.ArgumentParser(add_help=False, parents=[mirna_parser])
    output_style_group = converter_parser.add_mutually_exclusive_group()
    output_style_group.add_argument('--oneline', action='store_const', const='oneline', dest='out_format',
        default='oneline', help='Output style: Multi-mapped ids are separated by a semicolon (default)')
    output_style_group.add_argument('--newline', action='store_const', const='newline', dest='out_format',
        default='oneline', help='Output style: Multi-mapped ids are separated by a newline')
    output_style_group.add_argument('--tabsep', action='store_const', const='tabsep', dest='out_format',
        default='oneline', help='Output style: Tab-separated `original\tconverted` ids')

    # Abstract Type Converter Parser (`to_precursors` and `to_mirnas`)
    convert_type_parser = argparse.ArgumentParser(add_help=False, parents=[converter_parser])
    convert_type_parser.add_argument('-u', '--unique', action='store_const', const='unique', dest='conv_type',
        default='all', help='Only output ids that map uniquely')

    # Abstract Analysis Parser
    species_choices = ['hsa', 'mmu', 'rno', 'ath', 'bta', 'cel', 'dme', 'dre', 'gga', 'ssc']
    enrichment_parser = argparse.ArgumentParser(add_help=False, parents=[mirna_parser])
    enrichment_parser.add_argument('species', choices=species_choices, help='Species')
    enrichment_parser.add_argument('-x', '--no-results', action='store_true',
        help='Do not monitor progress or obtain results. Can retrieve later using Job ID.')
    categories_group = enrichment_parser.add_argument_group(*mutex_help_text(required=False))
    categories_group.add_argument('-c', '--categories', nargs='+', default=['default'],
        help='Set of categories to include in analysis, can include `all`, `default`, `expert` or specific categories')
    categories_group.add_argument('-C', '--categories-file', type=argparse.FileType('r'),
        help='File specifying categories to include in analysis')
    enrichment_parser.add_argument('-t', '--threshold', type=int, default=2, nargs=1,
        help='Filter out subcategories that contain less than this many miRNAs/precursors (default=2)')
    enrichment_parser.add_argument('-s', '--significance', '--alpha', type=float, default=0.05, nargs=1,
        help='Significance level (default=0.05)')
    enrichment_parser.add_argument('-g', '--group-adjust', action='store_false', dest='indep_adjust',
        help='Adjust p-values over aggregated groups (By default each group is adjusted independently)')
    enrichment_parser.add_argument('-a', '--adjustment', type=str, default='fdr', nargs=1,
        choices=['none', 'fdr', 'bonferroni', 'BY', 'holm', 'hochberg', 'hommel'],
        help="p-value adjustment method (default='fdr')")
    output_format_group = enrichment_parser.add_mutually_exclusive_group()
    output_format_group.add_argument('--csv', action='store_const', const='csv', dest='outfile_type',
        help="Store results in output file in csv format (default)")
    output_format_group.add_argument('--json', action='store_const', const='json', dest='outfile_type',
        help="Store results in output file in json format (default is csv)")
    enrichment_parser.set_defaults(outfile_type='csv')

    # Abstract Job Parser
    job_parser = argparse.ArgumentParser(add_help=False, parents=[base_parser])
    job_parser.add_argument('-j', '--jobid', type=str, dest='job_id', help='Job ID')

    # Concrete Subcommand Parsers
    # ---------------------------
    # ORA parser
    ora_parser = subparsers.add_parser('ora', parents=[enrichment_parser], help='Run Over-representation Analysis')
    reference_set_group = ora_parser.add_argument_group(*mutex_help_text(required=False))
    reference_set_group.add_argument('-r', '--reference-set', nargs='+',
        help='(Optional) Set of background miRNAs/precursors')
    reference_set_group.add_argument('-R', '--reference-set-file',
        help='(Optional) File specifying background miRNAs/precursors')
    ora_parser.set_defaults(parser_name='ora', call=enrichment_analsis)

    # GSEA parser
    gsea_parser = subparsers.add_parser('gsea', parents=[enrichment_parser], help='Run Gene Set Enrichment Analysis')
    gsea_parser.set_defaults(parser_name='gsea', call=enrichment_analsis)

    # miRNA->precursor
    to_prec_parser = subparsers.add_parser('to_precursor', parents=[convert_type_parser],
        help='Convert miRNAs to precursors')
    to_prec_parser.set_defaults(parser_name='to_precursor', call=type_converter)

    # precursor->miRNA
    to_mirna_parser = subparsers.add_parser('to_mirna', parents=[convert_type_parser],
        help='Convert precursors to miRNAs')
    to_mirna_parser.set_defaults(parser_name='to_mirna', call=type_converter)

    # mirbase converter parser
    version_parser = subparsers.add_parser('convert_mirbase', parents=[converter_parser],
        help='Convert mirBase version')
    version_parser.add_argument('from_', metavar='FROM', help='mirBase version to convert miRNAs/precursors from')
    version_parser.add_argument('--to', default=22,
        help='mirBase version to convert miRNAs/precursors from (default=22)')
    version_parser.set_defaults(parser_name='convert_mirbase', call=mirbase_converter)

    # open webtool in browser parser
    open_parser = subparsers.add_parser('open', help='Open MiEAA tool in browser', parents=[job_parser])
    open_parser.add_argument('open', choices=('input', 'progress', 'results'), help='Open MiEAA interface in browser')
    open_parser.set_defaults(parser_name='open', call=open_browser)

def main():
    # check for mutually exclusive arguments (basically ArgumentParser.add_mutually_exclusive_group)
    # implemented due to inability to combine custom title/descriptions in help flag
    def exclusivity_check(subparser, set_opt, file_opt, flag_letter, required=True):
        lower_flag = flag_letter.lower()
        upper_flag = flag_letter.upper()
        if (set_opt and file_opt):
            err_message = 'argument `-{}` not allowed with argument `-{}`'.format(lower_flag, upper_flag)
        elif required and not set_opt and not file_opt:
            err_message = 'one of the arguments `-{}` or `-{}` is required'.format(lower_flag, upper_flag)
        else:
            return
        subparser.print_usage()
        subparser.error(err_message)

    # Base parser requiring subcommands
    mieaa_parser = argparse.ArgumentParser(prog='miEAA', description='miEAA Command Line Tool')
    mieaa_parser.add_argument('--version', action='version', version='{} {}'.format(mieaa_parser.prog, __version__))
    mieaa_subparsers = mieaa_parser.add_subparsers()
    create_subcommands(mieaa_subparsers)

    args, unknown = mieaa_parser.parse_known_args()

    try:
        selected_parser = mieaa_subparsers.choices[args.parser_name]
    except AttributeError:  # parser_name won't be in the Namespace if no subcommand
        mieaa_parser.error('valid subcommand is required')

    if unknown:
        selected_parser.print_usage()
        selected_parser.error('unrecognized arguments: {}'.format(' '.join(unknown)))

    # check mutually exclusive flags
    try:
        exclusivity_check(selected_parser, args.mirna_set, args.mirna_set_file, 'm')
        if args.parser_name == 'ora' or args.parser_name == 'gsea':
            exclusivity_check(selected_parser, args.categories, args.categories_file, 'c', required=False)
        if args.parser_name == 'ora':
            exclusivity_check(selected_parser, args.reference_set, args.reference_set_file, 'r', required=False)
    except AttributeError:
        pass

    mieaa = API()
    results = args.call(mieaa, args)
    try:  # outfile not in all parsers
        if args.verbose or not args.outfile:
            print(results)
    except AttributeError:
        pass


if __name__ == "__main__":
    main()
