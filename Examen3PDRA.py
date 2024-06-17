import pandas as pd
import requests
import hashlib
import time
import sqlite3
import json
import os

url = "https://restcountries.com/v3.1/all"
response = requests.get(url)
countries_data = response.json()

country_names = []
language_names = []
language_hashes = []
processing_times = []

for country in countries_data:
    country_name = country.get('name', {}).get('common', 'Unknown')
    languages = country.get('languages', {})
    
    if languages:
        for language in languages.values():
            start_time = time.time()
            language_hash = hashlib.sha1(language.encode()).hexdigest()
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            country_names.append(country_name)
            language_names.append(language)
            language_hashes.append(language_hash)
            processing_times.append(processing_time)

data = {
    "Pais": country_names,
    "Idioma": language_names,
    "SHA1": language_hashes,
    "Tiempo": processing_times
}
df = pd.DataFrame(data)

total_time = df['Tiempo'].sum()
average_time = df['Tiempo'].mean()
min_time = df['Tiempo'].min()
max_time = df['Tiempo'].max()

print(f"Tiempo Total: {total_time}")
print(f"Tiempo Promedio: {average_time}")
print(f"Tiempo Min: {min_time}")
print(f"Tiempo Max: {max_time}")


conn = sqlite3.connect('examendra.db')
df.to_sql('countries', conn, if_exists='replace', index=False)
conn.close()
df.to_json('data.json', orient='records', indent=4)


