import requests
import yaml
import pandas as pd
import traceback

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

url = 'https://api.helsedirektoratet.no/ProduktCovid19/Covid19Statistikk/'

headers = {
    'Ocp-Apim-Subscription-Key': cfg['api']['key'],
}

def write_df(df):
    filename = traceback.extract_stack(None, 2)[0][2]
    df.to_csv('data/' + filename + '.csv', encoding='utf-8', index=False)
    df.to_excel('data/' + filename + '.xlsx', encoding='utf-8', index=False)

def admissions_nat():
    res = requests.get(url + 'nasjonalt', headers=headers).json()
    df = pd.DataFrame(res['registreringer'])
    df = df.rename(columns={'dato': 'date', 'antInnlagte': 'admissions', 'antRespirator': 'respiratory'})
    df = df[['date', 'admissions', 'respiratory']]
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df = df.sort_values(['date'], ascending=True)

    write_df(df)

def admissions_reg():
    res = requests.get(url + 'helseregion', headers=headers).json()
    df = pd.json_normalize(res, 'registreringer', ['navn'])
    df = df.rename(columns={'dato': 'date', 'navn': 'health_reg_name', 'antInnlagte': 'admissions', 'antRespirator': 'respiratory'})
    df = df[['date', 'health_reg_name', 'admissions', 'respiratory']]
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

    write_df(df)

def admissions_org():
    res = requests.get(url + 'helseforetak', headers=headers).json()
    df = pd.json_normalize(res, 'covidRegistreringer', ['helseforetakNavn', 'region'])
    df = df.rename(columns={'dato': 'date', 'helseforetakNavn': 'health_org_name', 'region': 'health_reg_name', 'antInnlagte': 'admissions', 'antRespirator': 'respiratory'})
    df = df[['date', 'health_reg_name', 'health_org_name', 'admissions']]
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df = df.sort_values(['health_reg_name', 'health_org_name', 'date'], ascending=True)

    write_df(df)

if __name__ == '__main__':
    admissions_nat()
    admissions_reg()
    admissions_org()