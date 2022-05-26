import os
import json
import requests
import pandas as pd
import time

class CBG():

        
    def get_url_response(self,url):
        inp = requests.get(url)
        resp = json.loads(inp.text)
        return resp

    def get_all_restaurants(self,lat,lng,radius):
        file = open('../config/config.json')
        config = json.load(file)
        api_key = config['goog_api_keys'][0]
        location = str(lat) + ',' + str(lng)
        base_search_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
        first_url = base_search_url+'key={}&location={}&radius={}&type=restaurant'.format(api_key,location,radius)
        resp = self.get_url_response(first_url)
        if 'error_message' in resp:
            api_key = config['goog_api_keys'][1]
            first_url = base_search_url+'key={}&location={}&radius={}&type=restaurant'.format(api_key,location,radius)
            resp = get_url_response(first_url)
            if 'error_message' in resp:
                return 'Error'
        results = (resp['results'])

        while 'next_page_token' in resp:
            time.sleep(10)
            next_page_token = resp['next_page_token']
            url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={}&key={}'.format(next_page_token,api_key)
            resp = self.get_url_response(url)
            results.extend(resp['results'])
        return results

    def write_cbg_json(self,radius, cbg, lat, lng):

        dpath = '../data/outputs/cbg_restaurants/'
        fname = dpath + str(cbg) + '_radius-' + str(round(radius)) + 'm' + '.json'
        if os.path.exists(dpath):
            file_list = [dpath + f for f in os.listdir(dpath)]
        else:
            file_list=[]
        if fname not in file_list:
            results = self.get_all_restaurants(lat, lng, radius)
            if results == 'Error':
                return 'Error'
            df = pd.DataFrame(results)
            df['CBG'] = cbg
            df['Radius'] = radius
            dpath = '../data/outputs/cbg_restaurants/'
            os.makedirs(dpath, exist_ok=True)
            # fname = dpath + str(cbg) + '_radius-' + str(round(radius)) + 'm' + '.json'
            df.to_json(fname, indent=6, orient='records')
            time.sleep(10)


