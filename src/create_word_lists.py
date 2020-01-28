import string
import re
import os
from  src.languages import gateway
import configparser

def _clean_text(raw_text, punctuation):
    '''
    #TODO throw into config file
    returns text stripped of symbols
    
    params:
        raw_text (string): the word to be cleaned up
    returns:
        string
    '''
    #TODO call config for punctuation
    return raw_text.translate(str.maketrans('', '', string.punctuation + u"\u00BF\u00A1\u2013\u2014"))

def _generate_word_list(text):
    '''breaks text files into individual words, cleans them before YIELDING
    
    params:
        text: the raw text of the file, no formatting ect.
    
    returns:
        string
    '''

    config = configparser.ConfigParser()
    config.read('default.ini')
    #TODO config punctuation
    punctuation = '' # config[language]["punctuation"]

    for line in text.split('\n'):
        for word in line.split():
            yield _clean_text(word.lower(), punctuation)

def gen_ch_lexicon(ch_path, word_list_path, language):
    '''
     writes unique lexicon for each chapter to an output file path 
     no vocab.from previous ch. will appear on successive lists
     
     params:
         ch_path (string) : path of where each chapter text file is stored 
         word_list_path (string) : path of where user wants word_lists to be written to
         
    returns:
        nothing
    '''
    list_of_files = os.listdir(ch_path) # paths for each chapter
    cumulative_lexicon = set() # to ensure unique terms for each chapter
    translator = getattr(gateway, language, None) # grab the correct translator

    for file in list_of_files:
        file_name = file.rstrip('.txt')
        with open(f'{ch_path}/{file}') as f:
            content = f.read()

            list_of_words = set(_generate_word_list(content)) - cumulative_lexicon
            
            cumulative_lexicon = cumulative_lexicon | list_of_words 
            
            list_of_translated_words = dict({(word, translator(word)) for word in list_of_words})
            
            with open(f'{word_list_path}/ch{file_name}_lexicon.txt', 'w') as f:
                f.write('\n'.join(f'{word} | {translated_word}' 
                    for word, translated_word in list_of_translated_words.items()))
    

def divide_by_chapter(input_file, ch_path, ch_delimiter):
    '''
    divides text file into chapters and writes each chapter to a text file

    params:
        out_path (string): where the folder that holds all the results will be
        ch_delimiter (string): what separates one chapter from the next in the input
            source material
    returns:
        writes result to given output files
    '''
    
    # read input file
    with open(input_file) as f:
        content = f.read()

        # list of chapters based off delimiter
        chapters = re.split(fr'{ch_delimiter}\s\d+\n', content)

    # write individual chapters to files
    for number, chapter_text in enumerate(chapters):
        with open(f'{ch_path}/{number}.txt', 'w') as f:
           f.write(chapter_text)

def gen_lexicon(input_file, language, user_options):
    '''
    gateway to generating lexicon
    params:
        input_file (string): input file path
        language (string): language we are translating from
        config (dict): has all the minutae needed to make this baby work
    returns:
        nothing, writes to an output
    '''
    
    # make use of user_options
    ch_delimiter = user_options['ch_delimiter']
    ch_path = user_options['paths']['chapter_path']
    lexicon_path = user_options['paths']['lexicon_path']
    # print(f'delimiter: {ch_delimiter} out_path: {out_path} ch_path: {ch_path}')

    divide_by_chapter(input_file,ch_path, ch_delimiter)
    gen_ch_lexicon(ch_path, lexicon_path, language)
