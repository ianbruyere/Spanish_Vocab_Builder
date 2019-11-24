from string import ascii_letters
from collections import defaultdict, namedtuple
import io, time, json
import unittest
import requests
from pathlib import Path
from bs4 import BeautifulSoup

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

TENSES = ['present', 'preterit', 'imperfect', 'imperfect2', 'conditional', 'future']
MOODS = ['indicative', 'subjunctive', 'imperative', 'continuous', 'perfect', 'perfectsubjunctive']
PRONOUNS = ['yo', 'tu', 'el/ella/usted', 'nosotros', 'vosotros', 'ellos/ellas/ustedes']

def spanish_dict_verb_conj_parser(verb):
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
        pass
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

#TODO split chapters and output to separate text files
def split_chapters(book):
    with b as open(book):
        content = b.read()
        for chapter in content.split()

# TODO argparser for different chapter delimiters
# TODO split by word, making sure each is unique
# TODO clean up words so only alpha characters remain, and 
# hyphenated words
# TODO for each unique word hook up to translator
# TODO build a library of conjugations, figures out what tense based 
# off of dictionary

