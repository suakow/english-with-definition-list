__author__ = "Puri Phakmongkol"
__author_email__ = "me@puri.in.th"

"""
* English with Definition List
*
* Created date : 03/05/2023
*
+      o     +              o
    +             o     +       +
o          +
    o  +           +        +
+        o     o       +        o
-_-_-_-_-_-_-_,------,      o
_-_-_-_-_-_-_-|   /\_/\
-_-_-_-_-_-_-~|__( ^ .^)  +     +
_-_-_-_-_-_-_-""  ""
+      o         o   +       o
    +         +
o      o  _-_-_-_- main.py
    o           +                     
+      +     o        o      +
"""

from selenium import webdriver
from bs4 import BeautifulSoup

import pandas as pd

from tqdm.auto import tqdm
import functools
import json

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver', options=chrome_options)

if __name__ == '__main__' : 
    oxford_3000 = open('oxford_3000.txt', 'r').read().split('\n')
    oxford_5000 = open('oxford_5000.txt', 'r').read().split('\n')

    oxford_3000 = oxford_3000 + oxford_5000

    vocab_list_3000 = []
    unsuccess = []
    oxford3000_loop = tqdm(oxford_3000)

    for _ in oxford3000_loop :
        try : 
            oxford3000_loop.set_description(f'Word: {_}')
            driver.get(f'https://dictionary.cambridge.org/dictionary/english/{_}')
            soup = BeautifulSoup(str(driver.page_source), 'html.parser')
            main_result = soup.find_all('div', class_='entry-body')[0]
            sub_result = main_result.find_all('div', class_='pr entry-body__el')
            for i in sub_result :
                pos = i.find('span', class_='pos dpos').text
                sound = i.find('span', class_='ipa').text
                try : 
                    cefr_level = i.find_all('div', class_='def-block')[0].find('span', class_='epp-xref').text
                except :
                    cefr_level = 'none'
                definition = functools.reduce(lambda x,y: x+y, [ _x.text for _x in i.find_all('div', class_='def-block')[0].find('div', class_='def ddef_d db').children ]).replace(': ', '') + '.'
                vocab_list_3000.append({
                    'vocab' : _,
                    'sound' : sound,
                    'pos' : pos,
                    'cefr_level' : cefr_level,
                    'definition' : definition,
                })

        except :
            unsuccess.append(_)
            continue

    vocab_3000_df = pd.DataFrame(vocab_list_3000)
    vocab_3000_df.to_csv('oxford_5000.csv', index=False)
    open('unsuccess.txt', 'w').write(json.dumps(unsuccess))
    
        