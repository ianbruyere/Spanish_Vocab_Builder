from src.languages.spanish import translate_word
import os 
import time

def open_file(lexicon_path):
    def inner_func(func):
        @wraps(func)
        def wrapped(*args):
            with open(lexicon_path, 'w') as f:
                return func(*args, **kwargs)
        return wrapped


def spanish(word): 
    #TODO config sleep value
    time.sleep(.090)
    return translate_word.word_trans_parser(word)
            
            

