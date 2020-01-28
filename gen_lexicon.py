#!/bin/env python

import os
import sys
import configparser
from src import cli 
from src.create_word_lists import gen_lexicon


# where all the functions gather together in harmony
#TODO how to make anki flash cards
#TODO implement testing suite
#TODO long-term: incorporating more languages, making resilient & versatile

# get arguments
parser = cli.create_arg_parser()
args = parser.parse_args()


# figure out defaults
#TODO 4 move config call into lexicon, rename config -> user_options, for flags and such
config = configparser.ConfigParser()
config.read('src/default.ini')

txt_input_path, language = args.txt_input_path[0], args.language.lower()

book_title = args.title if args.title != None else config['DEFAULT']['output']
ch_delimiter = config[language]['ch_delimiter'] if args.separator == None else args.separator

# pathing setup
if args.output != None: 
    if not os.path.exists(output_path):
        a = ''
        while a != 'y' or a != 'n':
            a = prompt("""An output directory was not given  or the one provided 
                was invalid. The output will be generated locally. 
                Do you want to procede?[Y/n] """).lower()

    if a.lower() == 'n':
        sys.exit()
output_path = os.getcwd()

# building the output paths
book_path = f'{output_path}/{book_title}'
ch_path = f'{book_path}/{config["DEFAULT"]["ch_out"]}'
lexicon_path = f'{book_path}/{config["DEFAULT"]["ch_lexicon_out"]}'
  
#TODO 4   
config = {'paths': {'output_path': book_path, 'chapter_path': ch_path, 'lexicon_path': lexicon_path}, "ch_delimiter": ch_delimiter}
    
# make directorys if they don't exist
for path in config['paths'].values():
   if not os.path.isdir(path):
        os.mkdir(path)

# passing in language because I think it could be useful as more are added in
gen_lexicon(txt_input_path, language, config) 

