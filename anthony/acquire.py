import numpy as np
from bs4 import BeautifulSoup
import requests
from requests import get
import pandas as pd
import numpy as np
import os
import time

def get_gitmds():     
    '''
    * Creates a list of urls from the top 100 most starred repos of both Python and Javascript code
    * Then for each url it scrapes the text from their readmes and code blocks to generate a json dictionary file 
    that looks like {"body":text from the readme, "top_code":the first entry from the code block}.
    * File name generated is gitMDs.json
    * If file exists it will read the file into a dataframe
    * If the file does not exist it will create the file (outlined above) and will return a dataframe of the file

    Note - The initial file creation time is ~33mins due to number of pages being scraped. 
    The file has been included in this repo due to that.
    '''
    # If the gitMDs.json file exists it will load a datafarme from it
    file = 'gitMDsv2.json'
    if os.path.isfile(file):
        gitmds = pd.read_json(file)
        return gitmds
    
    # If it does not exist it will create it, save it, and still load the dataframe
    else:
        # first 20 pages of the search from each JavaScript and Python search results
        repos = ['https://github.com/search?l=JavaScript&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=JavaScript&p=2&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=JavaScript&p=3&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=JavaScript&p=4&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=JavaScript&p=5&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=JavaScript&p=6&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=JavaScript&p=7&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=JavaScript&p=8&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=JavaScript&p=9&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=JavaScript&p=10&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=JavaScript&p=11&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=JavaScript&p=12&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=JavaScript&p=13&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=JavaScript&p=14&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=JavaScript&p=15&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=JavaScript&p=16&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=JavaScript&p=17&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=JavaScript&p=18&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=JavaScript&p=19&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=JavaScript&p=20&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=Python&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=Python&p=2&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=Python&p=3&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=Python&p=4&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=Python&p=5&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=Python&p=6&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=Python&p=7&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=Python&p=8&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=Python&p=9&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=Python&p=10&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=Python&p=11&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=Python&p=12&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=Python&p=13&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=Python&p=14&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=Python&p=15&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=Python&p=16&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=Python&p=17&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=Python&p=18&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=Python&p=19&q=stars%3A%3E0&s=stars&type=Repositories',
        'https://github.com/search?l=Python&p=20&q=stars%3A%3E0&s=stars&type=Repositories']
        
        #Base url used to create the urls from the repo scrape
        base_url = "https://github.com/"
        # empty urls list to store the results
        urls = []
        # for each repo link in the above list
        for repo in repos: 
            response = get(repo)
            soup = BeautifulSoup(response.content, 'html.parser')
            # create the a 'v-align-middle' text
            links = soup.findAll('a', class_='v-align-middle')
            # wait 3 seconds to avoid getting rate limited
            time.sleep(3)
            # then use a for loop to append each link the urls list
            for link in links:
                # combines the base_url and the link text to get the full link
                urls.append(base_url+link.text)  

        # create an empty list to get store the results of scrapping the readme
        github = []
        # for each url in the urls list
        for url in urls:
            response = get(url)
            soup = BeautifulSoup(response.content, 'html.parser') 
            # tries to get the text from the markdown-body
            try:
                body = soup.find('article', class_='markdown-body entry-content container-lg').text
            # if the markdown-body doesn't exist or another error is given continue to the next iteration in the loop
            except AttributeError:
                continue
            # assigns the first codeblock result to code
            code = soup.find('a', class_='d-inline-flex flex-items-center flex-nowrap link-gray no-underline text-small mr-3').text
            # creates a dictionary object of the body and top_code text
            dicob = {'body':body, 'top_code':code}
            # appends the result to the gihub list
            github.append(dicob)
            # waits three seconds to avoid getting rate limited
            time.sleep(5)

        # takes the github dictionary list and turns it into a dataframe
        gitmds = pd.DataFrame(github)
        # takes the newly formed dataframe and saves it as a gitMDs.json
        gitmds.to_json('gitMDs.json')
        # returns the dataframe
        return gitmds