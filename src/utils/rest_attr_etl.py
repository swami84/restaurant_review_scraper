import copy
import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from os.path import exists

import json
class rest_attr():
    def __init__(self):
        self.driver = self.__get_driver()

    def __get_driver(self, debug=False):
        options = Options()

        if not debug:
            options.add_argument("--headless")
            options.add_argument('--no-sandbox')
        else:
            options.add_argument("--window-size=1366,768")
            options.add_argument('--no-sandbox')

        options.add_argument("--disable-notifications")
        options.add_argument('--disable-gpu')
        options.add_argument("--lang=en-US")
        driv_path = '../config/webdrivers/chromedriver.exe'
        input_driver = webdriver.Chrome(options=options, executable_path=driv_path)

        return input_driver

    def get_rest_info(self, cbg,place_id, rest_name, rest_add,i=None):
        path_to_file = '../data/outputs/rest_attrs/rest_attrs_compiled.json'
        if exists(path_to_file):
            rest_attrs = json.load(open(path_to_file))

            if any(d['place_id'] == place_id for d in rest_attrs):
                return None
        rest_name = rest_name.replace('&', '+%26+')
        url = 'https://www.google.com/search?q=' + rest_name + ' ' + rest_add


        self.driver.get(url)
        time.sleep(1)
        rest_dict = {}
        rest_dict['cbg'] = cbg
        rest_dict['place_id'] = place_id
        response = BeautifulSoup(self.driver.page_source, 'html.parser')
        map_url = None
        for res in response.find_all('a', href=True):
            if 'maps.google' in res['href']:
                map_url = res['href']
        if map_url:
            self.driver.get(map_url)
        else:
            return None
        for res in self.driver.find_elements_by_xpath('//button[@jsaction=\'pane.rating.category\']'):

            rest_dict['rest_type'] = res.text

        for res in self.driver.find_elements_by_xpath('//button[@jsaction=\'pane.rating.moreReviews\']'):
            reviews_text = res.text
            if 'reviews' in reviews_text:
                rest_dict['no_of_reviews'] = int(reviews_text.split('reviews')[0].replace(',', ''))
            else:
                rest_dict['no_of_reviews'] = int(res.text[:2])

        resp = BeautifulSoup(self.driver.page_source, 'html.parser')

        for res in resp.find_all('span', jsinstance="*1"):
            if '$' in res.text:

                rest_dict['price_range_$'] = len(res.text.split('·')[1])
        for res in self.driver.find_elements_by_xpath('//button[starts-with (@jsaction,\'pane.attributes.expand\')]'):
            rest_summary_text = res.text.split('\n')
            rest_dict['rest_summary'] = rest_summary_text[0]
            rest_dict['rest_labels'] = [lab for lab in rest_summary_text[1:] if lab != '·']
        for res in resp.find_all('div', class_="O9Q0Ff-NmME3c-Utye1-Fq92xe O9Q0Ff-NmME3c-Utye1-Fq92xe-visible"):
            rest_pop_time = (res.find_all('div', class_ = 'O9Q0Ff-NmME3c-Utye1-ZMv3u O9Q0Ff-NmME3c-Utye1-ZMv3u-SfQLQb-V67aGc'))
            for r in rest_pop_time:
                if 'at' in r['aria-label']:
                    time_int = r['aria-label'].split('at ')[1].replace('.','')
                    rest_dict[time_int] = r['aria-label'].split('%')[0]
        path_to_file = '../data/outputs/rest_attrs/rest_attrs_' + str(i) + '.json'
        if  len(rest_dict) >0:
            self.write_rest_attr(rest_dict, path_to_file)
        return rest_dict

    def write_rest_attr(self,rest_dict,path_to_file):


        if not exists(path_to_file):

            rest_attrs = []
        else:
            rest_attrs = json.load(open(path_to_file))
        if not any(d['place_id'] == rest_dict['place_id'] for d in rest_attrs):
            rest_attrs.append((rest_dict))

            with open(path_to_file, 'w') as outfile:
                json.dump(rest_attrs, outfile, indent=6)



