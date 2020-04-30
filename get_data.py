import requests
import yaml
import pandas as pd
from pandas.io.json import json_normalize

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

url = 'https://api.helsedirektoratet.no/ProduktCovid19/Covid19Statistikk/'

headers = {
    'Ocp-Apim-Subscription-Key': cfg['api']['key'],
}

def health_nat():
    res = requests.get(url + 'nasjonalt', headers=headers).json()
    df = pd.DataFrame(res['registreringer'])
    df = df.rename(columns={'dato': 'date', 'antInnlagte': 'admissions', 'antRespirator': 'respiratory'})
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df = df.sort_values(['date'], ascending=True)
    df.to_csv('data/admissions_nat.csv', encoding='utf-8', index=False)
    df.to_excel('data/admissions_nat.xlsx', encoding='utf-8', index=False)

def health_reg():
    res = requests.get(url + 'helseregion', headers=headers).json()
    df = json_normalize(res, 'registreringer', ['navn'])
    df = df.rename(columns={'dato': 'date', 'navn': 'health_reg_name', 'antInnlagte': 'admissions', 'antRespirator': 'respiratory'})
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df.to_csv('data/admissions_reg.csv', columns=['date', 'health_reg_name', 'admissions', 'respiratory'], encoding='utf-8', index=False)
    df.to_excel('data/admissions_reg.xlsx', columns=['date', 'health_reg_name', 'admissions', 'respiratory'], encoding='utf-8', index=False)

def health_org():
    res = requests.get(url + 'helseforetak', headers=headers).json()
    df = json_normalize(res, 'covidRegistreringer', ['helseforetakNavn', 'region'])
    df = df.rename(columns={'dato': 'date', 'helseforetakNavn': 'health_org_name', 'region': 'health_reg_name', 'antInnlagte': 'admissions', 'antRespirator': 'respiratory'})
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df = df.sort_values(['health_reg_name', 'health_org_name', 'date'], ascending=True)
    df.to_csv('data/admissions_org.csv', columns=['date', 'health_reg_name', 'health_org_name', 'admissions'], encoding='utf-8', index=False)
    df.to_excel('data/admissions_org.xlsx', columns=['date', 'health_reg_name', 'health_org_name', 'admissions'], encoding='utf-8', index=False)

if __name__ == '__main__':
    health_nat()
    health_reg()
    health_org()