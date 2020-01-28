import argparse

def create_arg_parser():
    """
    where the arg parser comes out to play
    """
    parser = argparse.ArgumentParser(description='Translate Unique Lexicon for Each Chapter')
    
    # positional arguments
    parser.add_argument('txt_input_path', nargs=1, metavar='TEXT_INPUT_FILE_PATH', type=str,
            help='the file path of the input book text')

    parser.add_argument('language', type=str, metavar='LANGUAGE',
            help='language of input material')

    # optional arguments
    parser.add_argument('-t', '--title', type=str, metavar='TITLE', help='book title')

    parser.add_argument('-o', '--output', type=str, metavar='OUTPUT_PATH', 
            help='where to output final results(split chapters, chapter lexicon, translations)'
            )

    parser.add_argument('-s', '--separator', type=str, metavar='SEPARATOR',
            help='''determines what the chapters will be split on. 
            Defaults to selected languages "chapter" 
            (eg Spanishs default is capitulo)'''
            )

    return parser

def call_translator(args=None, stdout=False):
    parser = create_arg_parser()

    if args is None:
        args = parser.parse_args()


