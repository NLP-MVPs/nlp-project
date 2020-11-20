import pandas as pd 
import numpy as np
import unicodedata
import re
import json
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
from acquire import get_gitmds

def basic_body_clean(somestring):
    '''
    Takes in body text of a README and performs a basic clean by first converting it to all lower case letters,
    then normalizes the encoding, and removes any character that isn't a letter, number, or a space.
    Returns the result.
    '''
    basic = somestring.lower()
    basic = unicodedata.normalize('NFKD', basic).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    basic = re.sub(r"[^a-z0-9'\s]", '', basic)
    return basic

def basic_code_clean(somestring):
    '''
    Takes in the code text and performs a basic clean by first converting it to all lower case letters,
    then normalizes the encoding, and finally removes any character that isn't a letter, number, period (.), or a space.
    Keeps the period because the code block text is expressed as a percentage with a period
    Returns the result.
    '''
    basic = somestring.lower()
    basic = unicodedata.normalize('NFKD', basic).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    basic = re.sub(r"[^a-z0-9'\s.]", '', basic)
    return basic

def tokenize(somestring):
    '''
    Creates a tokenizer object to tokenize the given string and then returns the tokenized string
    '''
    tokenizer = nltk.tokenize.ToktokTokenizer()
    tokened = tokenizer.tokenize(somestring, return_str=True)    
    return tokened

def lemmatize(somestring):
    '''
    Creates a lemmatize object and then uses it to lemmatize the provided string. Returns the lemmatized string 
    '''
    wnl = nltk.stem.WordNetLemmatizer()
    lemmas = [wnl.lemmatize(word) for word in somestring.split()]
    article_lemmatized = ' '.join(lemmas)
    return article_lemmatized

def remove_stopwords(string, keep_words=['no', 'not'], exclude_words=[]):
    '''
    This function takes in a string, removes stop_words from the string, and then returns the results.
    The fuction also allows for optional arugments keep_words and exclud_words to modify the stop word list
    * keep_words - a list of words to remove from the standard english stopwords list from nltk.corpus i.e. no or not
    * exclude_words - a list of words to add to the standard english stopwords list from nltk.corpus 
    i.e. ['data', 'science'] to the remove both words when dealing with articles only about data science
    * By default, keep_words includes no and not
    '''
    # Create stopword_list.
    stopword_list = stopwords.words('english')
    # Remove 'keep_words' from stopword_list to keep these in my text.
    stopword_list = set(stopword_list) - set(keep_words)
    # Add in 'exclude_words' to stopword_list.
    stopword_list = stopword_list.union(set(exclude_words))
    # Split words in string.
    words = string.split()
    # Create a list of words from my string with stopwords removed and assign to variable.
    filtered_words = [word for word in words if word not in stopword_list]
    # Join words in the list back into strings and assign to a variable.
    string_without_stopwords = ' '.join(filtered_words)
    return string_without_stopwords

def prep_gitMDs():
    '''
    Uses the helper functions contained within the prepare.py module on the gitMDs repo url list from the acquire.py module to create a unified data frame for exploration
    * Applies a basic_body_clean, tokenizizatize, removestop_words, AND lemmatizes fuctions to the readme body text
      and returns the output as df['clean'].
    * Applies the basic_code_clean, tokenizizatize, and removestop_words fuctions to the top_code 
      and returns it as df['top_code_cleaned]
    * Splits df['top_code_cleaned] into two columns df['top_code_cleaned'] and df['top_percentage_cleaned']
    * Returns the gitMDs as a data frame
    '''    
    gitMDs = pd.DataFrame(get_gitmds())
    gitMDs['clean'] = gitMDs['body'].apply(basic_body_clean).apply(tokenize).apply(remove_stopwords).apply(lemmatize)
    gitMDs['top_code_clean'] = gitMDs['top_code'].apply(basic_code_clean).apply(tokenize).apply(remove_stopwords)
    gitMDs[['top_code_clean', 'percentage']] = gitMDs['top_code_clean'].str.split(" ",expand=True)
    gitMDs['percentage'] = pd.to_numeric(gitMDs['percentage'])
    return gitMDs
