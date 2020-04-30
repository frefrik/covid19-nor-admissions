# covid19-nor-admissions

## Description
The Norwegian Directorate of Health (Helsedirektoratet) offers an API on the dataset that is used to display daily updated figures on the number of patients admitted to hospitals with proven covid-19 and the number of hospitalized patients receiving respiratory care.

This script extracts COVID19 admissions data from the API and saves the results in .csv and .xlsx format.

The official view of the data is available here: https://www.helsedirektoratet.no/statistikk/antall-innlagte-pasienter-pa-sykehus-med-pavist-covid-19

## Usage
Get your API-key: https://utvikler.helsedirektoratet.no/

Rename config.dist.yml to config.yml and replace `APIKEY` with your API-key
```yaml
# config.yml
api:
  key: APIKEY
```

Run script:
```
$ python3 get_data.py
```

The output will be saved to `data/`