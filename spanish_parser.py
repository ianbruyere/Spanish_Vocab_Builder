import io, time, json, os, re
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

def generate_word_list(text):
    '''
    takes in string, yields every single word. To be called
    after text has been cleaned up right before calling translate on each word
    '''
    for line in content.split('\n'):
        for word in line.split():
            yield word.lower()

def get_unique_word_list(file_path):
    pass

def divide_chapters(text_file, chapter_delimiter_regex, output_dir="chapters"):
    '''
    divides .txt file into chapters and outputs 
    '''
    
    # pathing setup
    current_dir = os.getcwd()
    output_path = f'{current_dir}/{output_dir}'
    
    
    # make directory if it doesn't already exist
    if not os.path.isdir(output_path):
        os.mkdir(output_path)
    
    with open(text_file) as f:
        content = f.read()
        chapters = re.split(r'CAPÍTULO\s\d+\n', content)
    for number, chapter_text in enumerate(chapters):
        with open(f'{output_path}/{number}.txt', 'w') as f:
            f.write(chapter_text)
            

def clean_text(raw_text):
    '''
    returns text stripped of symbols
    '''
    pass

# TODO argparser for different chapter delimiters
# TODO split by word, making sure each is unique
# TODO clean up words so only alpha characters remain, and 
# hyphenated words
# TODO for each unique word hook up to translator
# TODO build a library of conjugations, figures out what tense based 
# off of dictionary

