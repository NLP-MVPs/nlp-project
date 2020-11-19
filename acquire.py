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
    Creates a list of various GitRepos urls from various news media orginizations, and then scrapes the text from their readmes and codes
    block to generate a json dictionary file that looks like {"body":text from the readme, "top_code":the first entry from the code block}.
    * File name generated is gitMDs.json
    * If file exists it will read the file into a dataframe
    * If the file does not exist it will create the file (outlined above) and will return the dataframe

    Note - The initial file creation time is ~3min and 30secs. The file has been included in this repo due to that.
    '''

    url = ['https://github.com/pewresearch/pewanalytics', 'https://github.com/texastribune/scuole', 'https://github.com/texastribune/thermometer', 'https://github.com/texastribune/walls', 'https://github.com/texastribune/geoip2', 'https://github.com/texastribune/queso-tools', 'https://github.com/texastribune/django-locking', 'https://github.com/texastribune/data-visuals-create', 'https://github.com/texastribune/tacobots', 'https://github.com/newscorp-ghfb/validates_timeliness','https://github.com/newscorp-ghfb/rbenv-cookbook','https://github.com/newscorp-ghfb/geogle']
    url2 = ['https://github.com/pewresearch/pewtils', 'https://github.com/pewresearch/search_sampler', 'https://github.com/gawkermedia/kinja-post-gem', 'https://github.com/bloomberg/chef-bcpc', 'https://github.com/bloomberg/locking_resource-cookbook', 'https://github.com/bloomberg/collectd-cookbook', 'https://github.com/bloomberg/nginx-cookbook', 'https://github.com/bloomberg/consul-cluster-cookbook', 'https://github.com/bloomberg/cobbler-cookbook', 'https://github.com/bloomberg/openbfdd-cookbook', 'https://github.com/newscorp-ghfb/kaminari']
    url3 = ['https://github.com/bloomberg/chef-bcs', 'https://github.com/bloomberg/zookeeper-cookbook', 'https://github.com/bloomberg/confd-cookbook', 'https://github.com/bloomberg/collectd_plugins-cookbook', 'https://github.com/bloomberg/kubernetes-cluster-cookbook', 'https://github.com/nytimes/nytcampfin', 'https://github.com/techcrunch/json_printer', 'https://github.com/observermedia/realgraph-listener', 'https://github.com/observermedia/django-wordpress-rest', 'https://github.com/thenextweb/passgenerator']
    url4 = ['https://github.com/thenextweb/amp-wp', 'https://github.com/thenextweb/laravel-elasticsearch', 'https://github.com/thenextweb/slack-laravel', 'https://github.com/thenextweb/craft-3-adminbar', 'https://github.com/npr/frank', 'https://github.com/thenextweb/Embed', 'https://github.com/thenextweb/oembed', 'https://github.com/thenextweb/flatten', 'https://github.com/thenextweb/curl', 'https://github.com/npr/php-image-optim', 'https://github.com/texastribune/top10pct', 'https://github.com/texastribune/newsapps-app-kit']
    url5 = ['https://github.com/thenextweb/cro', 'https://github.com/npr/node-randomstring', 'https://github.com/texastribune/tx_salaries', 'https://github.com/texastribune/the-dp', 'https://github.com/texastribune/tx_lege_districts', 'https://github.com/texastribune/tt_social_auth', 'https://github.com/texastribune/armstrong.core.tt_sections', 'https://github.com/texastribune/aeis', 'https://github.com/texastribune/ox-scale', 'https://github.com/texastribune/django-gistpage', 'https://github.com/newscorp-ghfb/sidekiq-throttler']
    url6 = ['https://github.com/theatlantic/django-nested-admin', 'https://github.com/theatlantic/django-xml', 'https://github.com/theatlantic/django-select2-forms', 'https://github.com/theatlantic/django-admin-locking', 'https://github.com/texastribune/lethal-drug-tracker', 'https://github.com/texastribune/txlege-camera-status', 'https://github.com/texastribune/postcss-amp', 'https://github.com/texastribune/talk', 'https://github.com/texastribune/code-grabber', 'https://github.com/texastribune/react-external-boilerplate']
    url7 = ['https://github.com/voxmedia/vc-ikea-minisite', 'https://github.com/voxmedia/viz-app', 'https://github.com/voxmedia/prebid.github.io', 'https://github.com/voxmedia/Transcriber', 'https://github.com/voxmedia/userstamp', 'https://github.com/voxmedia/gliss', 'https://github.com/nbcnews/octopus-vr', 'https://github.com/texastribune/donations-app', 'https://github.com/texastribune/djangocms-text-ckeditor', 'https://github.com/texastribune/newsapps-styleguide-2.0', 'https://github.com/texastribune/500', 'https://github.com/WSJ/pinpoint-editor', 'https://github.com/WSJ/ballot-tally']
    url8 = ['https://github.com/texastribune/txlege84', 'https://github.com/texastribune/donation-builder', 'https://github.com/abcnews/scrollyteller', 'https://github.com/abcnews/odyssey-scrollyteller', 'https://github.com/abcnews/data-life', 'https://github.com/abcnews/interactive-ssm-map', 'https://github.com/ajam/chartbuilder-electron', 'https://github.com/WSJ/scroll-watcher', 'https://github.com/WSJ/two-step', 'https://github.com/texastribune/faces-of-death-row', 'https://github.com/texastribune/text-balancer', 'https://github.com/WSJ/squaire']
    url9 = ['https://github.com/WSJ/the-meta-tag-checker', 'https://github.com/npr/nprapi-wordpress', 'https://github.com/npr/npr-one-backend-proxy-php', 'https://github.com/npr/pmp-wordpress-plugin', 'https://github.com/npr/pmp-php-sdk', 'https://github.com/npr/pmp-drupal-plugin', 'https://github.com/npr/zaphpa', 'https://github.com/npr/silverstripe-opauth', 'https://github.com/npr/Slim']
    urls= url+url2+url3+url4+url5+url6+url7+url8+url9
    
    file = 'gitMDs.json'
    if os.path.isfile(file):
        gitmds = pd.read_json(file)
        return gitmds
    
    else:
        github = []
        for url in urls:
            response = get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            body = soup.find('article', class_='markdown-body entry-content container-lg').text
            code = soup.find('a', class_='d-inline-flex flex-items-center flex-nowrap link-gray no-underline text-small mr-3').text
            dicob = {'body':body, 'top_code':code}
            github.append(dicob)
            time.sleep(2)

        gitmds = pd.DataFrame(github)
        gitmds.to_json('gitMDs.json')
        return gitmds