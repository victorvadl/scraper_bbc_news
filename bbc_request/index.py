import requests
import json
import pandas as pd
import configparser

# Load the keyword from the configuration file
config = configparser.ConfigParser()
config.read('config.cfg')

url = "http://localhost:5000/search"
params = {'keyword': config.get('API', 'keyword')}

try:
    response = requests.get(url, params=params)
    response.raise_for_status()
   
    data = response.json()
    df = pd.DataFrame(data)
    df.to_csv('D:/Projetos/Pessoal/scraper_bbc/bbc_request/output_data/output_api.csv', index=False, encoding='utf-8')


    with open('D:/Projetos/Pessoal/scraper_bbc/bbc_request/output_data/output_api.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)
        
except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
except json.JSONDecodeError as e:
    print(f"JSON decoding error: {e}")
except Exception as e:
    raise e
