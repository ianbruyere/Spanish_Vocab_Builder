import io, time, json, os, re, string
import unittest
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from collections import defaultdict, namedtuple

def retrieve_html(url):
    """
    Return raw HTML at specified url
    
    Args:
        url (string)
        
    Returns:
        status_code (integer):
        raw_html (string): the raw HTML content of the response, properly encoded according to the HTTP headers.
    """
    r = requests.get(url)
    return r.status_code, r.text

PRONOUNS = ['yo', 'tu', 'el/ella/usted', 'nosotros', 'vosotros', 'ellos/ellas/ustedes']

def verb_conj_parser(verb):
    '''
    Parses a verb page from HTML from Spanish Dictionary.com
    Args:
        verb (string) - spanish unconjugated verb
    Returns:
          Example Structure:
    namedTuple(Verb:str, conjugations)
    conjugations structure(dict of dict of dict):
      {
      'Mood_1':
        {
            'tense_1': {  'yo': conj, 'tu': tu_conj, etc },
            'tense_2': {  'yo': conj, 'tu': tu_conj, etc },
        },
      'Mood_2':
        {
            'tense_1': {  'yo': conj, 'tu': tu_conj, etc },
            'tense_2': {  'yo': conj, 'tu': tu_conj, etc },
        },
    '''
    status, html = retrieve_html(f'https://www.spanishdict.com/conjugate/{verb}')
    try:
        soup = BeautifulSoup(html, 'html.parser')
    except:
        return status
        # things happen
    conjugations = defaultdict(dict)
    table_cells = soup.find_all('div', {'class' : 'vtable-word-contents'})
    Verb = namedtuple('Verb', 'spanish english')
    for cell in table_cells:
        info = cell.find('a', {'class' : 'vtable-word-text'})
        if info is None:
            # decided not all were going to be links
            info = cell.find('div', {'class' : 'vtable-word-text'})
            if info is None:
                continue

        pronoun = PRONOUNS[int(info['data-person'])]
        # english = "info['data-original-title'] "
        english = ''
        # print(info.)
        tense = info['data-tense']
        verb = Verb(info.text, english)
        conjugations[tense].update({pronoun: verb})
    return conjugations

def word_trans_parser(spanish_word):
    '''
    returns translation of word from spanish -> english
    Args:
      word(string) - spanish word
    Returns:
        word(string) - english translation of given word
    '''
    status, html = retrieve_html(f'https://www.spanishdict.com/translate/{spanish_word}')
    try:
        soup = BeautifulSoup(html, 'html.parser')
    except:
        return status
    Translation = namedtuple('translation', 'spanish english')
    english_word = soup.find('div', {"id" : "quickdef1-es"})
    translation = Translation(spanish_word, english_word)
    return translation

def _clean_text(raw_text):
    '''returns text stripped of symbols'''
    return raw_text.translate(str.maketrans('', '', string.punctuation))

def _generate_word_list(text):
    '''
    takes in string, yields every single word. To be called
    after text has been cleaned up right before calling translate on each word
    '''
    for line in text.split('\n'):
        for word in line.split():
            yield _clean_text(word.lower())

def generate_chapter_word_lists(chapter_path, word_list_path):
    '''
     will loop through the chapter file path and generate a unique
     word list for each chapter 
     #TODO now I need to make it so there are no repeats from chapter to chapter, also remove upside 
     down question marks and dashes
    '''
    list_of_files = os.listdir(chapter_path)
    
    for file in list_of_files:
        with open(f'{chapter_path}/{file}') as f:
            content = f.read()
            list_of_words = list(set(_generate_word_list(content)))
            file_name = file.rstrip('.txt')
            with open(f'{word_list_path}/chapter_{file_name}_word_list.txt', 'w') as f:
                f.write('\n'.join(list_of_words))
    

def divide_book_into_chapters(text_file, chapter_delimiter_regex, output_path, title="default"):
    '''
    divides .txt file into chapters and outputs into given directory
    '''
    
    with open(text_file) as f:
        content = f.read()
        chapters = re.split(fr'{chapter_delimiter_regex}\s\d+\n', content)
    for number, chapter_text in enumerate(chapters):
        with open(f'{output_path}/{number}.txt', 'w') as f:
            f.write(chapter_text)
def main():
    '''
    where all the functions gather together in harmony
    '''

    #TODO add spanish translation for  each word list 
    #TODO look up how to make anki flash cards
    #TODO CLI
    
    book_title = 'el_leon_la_bruja_y_el_ropero'
    chapter_file_name = "chapters" 
    chapter_word_lists = "chapter_word_lists"
    
    # pathing setup
    current_dir = os.getcwd()
    book_path = f'{current_dir}/{book_title}'
    chapter_path = f'{book_path}/{chapter_file_name}'
    word_list_path = f'{book_path}/{chapter_word_lists}'
    
    paths_list = [book_path, chapter_path, word_list_path]
    
    # make directorys if they doesn't exist
    for path in paths_list:
        if not os.path.isdir(path):
            os.mkdir(path)
    
    divide_book_into_chapters('text.txt', 'CAPÍTULO', chapter_path)
    
    generate_chapter_word_lists(chapter_path, word_list_path)

# TODO argparser for different chapter delimiters
# TODO split by word, making sure each is unique
# TODO clean up words so only alpha characters remain, and 
# hyphenated words
# TODO for each unique word hook up to translator
# TODO build a library of conjugations, figures out what tense based 
# off of dictionary

