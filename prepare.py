import acquire
import pandas as pd 
import numpy as np
import unicodedata
import re
import json
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

def basic_body_clean(bodytext):
    '''
    Takes in body text of a README and performs a basic clean by first converting it to all lower case letters,
    then normalizes the encoding, and removes any character that isn't a letter, number, or a space.
    Returns the result.
    '''
    basic = somestring.lower()
    basic = unicodedata.normalize('NFKD', basic).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    basic = re.sub(r"[^a-z0-9'\s]", '', basic)
    return basic

def basic_code_clean(codetext):
    '''
    Takes in the code text and performs a basic clean by first converting it to all lower case letters,
    then normalizes the encoding, and finally removes any character that isn't a letter, number, period (.), or a space.
    Keeps the period because the code block text is expressed as a percentage with a period
    Returns the result.
    '''
    basic = somestring.lower()
    basic = unicodedata.normalize('NFKD', basic).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    basic = re.sub(r"[^a-z0-9'\s]", '', basic)
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

def remove_stopwords(string, extra_words=[], exclude_words=[]):
    '''
    This function takes in a string, removes stop_words from the string, and then returns the results.
    The fuction also allows for optional arugments extra_words and exclud_words to modify the stop word list
    * extra_words - a list of words to remove from the standard english stopwords list from nltk.corpus i.e. no or not
    * exclude_words - a list of words to add to the standard english stopwords list from nltk.corpus 
    i.e. ['data', 'science'] to the remove both words when dealing with articles only about data science
    '''
    # Create stopword_list.
    stopword_list = stopwords.words('english')
    # Remove 'exclude_words' from stopword_list to keep these in my text.
    stopword_list = set(stopword_list) - set(exclude_words)
    # Add in 'extra_words' to stopword_list.
    stopword_list = stopword_list.union(set(extra_words))
    # Split words in string.
    words = string.split()
    # Create a list of words from my string with stopwords removed and assign to variable.
    filtered_words = [word for word in words if word not in stopword_list]
    # Join words in the list back into strings and assign to a variable.
    string_without_stopwords = ' '.join(filtered_words)
    return string_without_stopwords

def prep_github():
    '''
    Uses the above helper on the github repo url list to creates to
    * Applies a basic_body_clean, tokenizizatize, removestop_words, AND lemmatizes fuctions to the readme body text
    and returns the output as df['clean'] 
    * Applies the basic_code_clean, tokenizizatize, and removestop_words fuctions to the top_code and returns it as df['top_code_cleaned]
    * Splits df['top_code_cleaned] into two columns df['top_code_cleaned'] and df['top_percentage_cleaned'] extended
    * returns the df
    '''    
    github = pd.DataFrame(acquire.get_github())
    github['clean'] = github['body'].apply(basic_body_clean).apply(tokenize).apply(remove_stopwords).apply(lemmatizes)
    github['top_code_clean'] = github['top_code'].apply(basic_code_clean).apply(tokenize).apply(remove_stopwords)
    github['percentage'] = pd.to_numeric(github['percentage'])
    return github
