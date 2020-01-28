import requests
import sys
import re
from bs4 import BeautifulSoup
from collections import defaultdict, namedtuple


PRONOUNS = ['yo', 'tu', 'el/ella/usted', 'nosotros', 'vosotros', 'ellos/ellas/ustedes']

def retrieve_html(url):
    """
    Return raw HTML at specified url
    
    params:
        url (string)
        
    Returns:
        status_code (integer):
        raw_html (string): the raw HTML content of the response, properly encoded according to the HTTP headers.
    """
    r = requests.get(url)
    return r.status_code, r.text


def verb_conj_parser(verb):
    '''
    Parses a verb page from HTML from Spanish Dictionary.com
    
    params:
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
        # english = "info['data-original-title']"
        english = ''
        tense = info['data-tense']
        verb = Verb(info.text, english)
        conjugations[tense].update({pronoun: verb})

    return conjugations
        
def word_trans_parser(spanish_word):
    '''
    returns translation of word from spanish -> english
    
    params:
      word(string) - spanish word
    Returns:
        word(string) - english translation of given word
    '''
    status, html = retrieve_html(f'https://www.spanishdict.com/translate/{spanish_word}')
    
    #TODO bust this out to a function
    if not re.fullmatch(r'20\d', str(status)):
        print(f'Connection to translation service is having the following error: {status}')
        sys.exit()

    try:
        soup = BeautifulSoup(html, 'html.parser')
    except:
        return status
    
    english_word = soup.find('div', {"id" : "quickdef1-es"})


    return english_word.text if english_word is not None else None 
