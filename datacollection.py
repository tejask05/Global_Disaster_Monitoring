import pandas as pd
import requests
import datetime
import spacy
import numpy as np
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from pymongo import MongoClient
from pymongo.server_api import ServerApi

NEWSAPI_KEY = 'ENTER YOUR API KEY HERE'
NEWSAPI_ENDPOINT = 'https://newsapi.org/v2/everything'

disaster_keywords = ['earthquake', 'flood', 'tsunami', 'hurricane', 'wildfire', 'forestfire', 'tornado', 'cyclone', 'volcano', 'drought', 'landslide', 'storm', 'blizzard', 'avalanche', 'heatwave']

# Load the spaCy English language model
nlp = spacy.load("en_core_web_sm")

# Initialize geocoder
geolocator = Nominatim(user_agent="my_geocoder")

def fetch_live_data(keyword):
    # Calculate the date 2 days ago
    two_days_ago = datetime.datetime.now() - datetime.timedelta(days=2)
    
    params = {
        'apiKey': NEWSAPI_KEY,
        'q': keyword,
        'from': two_days_ago.strftime('%Y-%m-%d'),  # From 1 days ago
        'to': datetime.datetime.now().strftime('%Y-%m-%d'),  # To today
        'language': 'en',
    }

    response = requests.get(NEWSAPI_ENDPOINT, params=params)
    return response.json().get('articles', [])

def identify_disaster_event(title):
    if title is None:
        return 'Unknown'
    
    # Identify the type of disaster event based on keywords
    
    return 'Unknown'

def extract_location_ner(text):
    doc = nlp(text)
    location_ner_tags = [ent.text for ent in doc.ents if ent.label_ == 'GPE']
    return location_ner_tags

def get_coordinates(location):
    try:
        location_info = geolocator.geocode(location, timeout=10) # Increase timeout if needed
        if location_info:
            return location_info.latitude, location_info.longitude
        else:
            return (np.nan, np.nan)
    except GeocoderTimedOut:
        print(f"Geocoding timed out for {location}")
        return (np.nan, np.nan)
    except Exception as e:
        print(f"Error geocoding {location}: {str(e)}")
        return (np.nan, np.nan)

if __name__ == "__main__":
    all_live_data = []
    for keyword in disaster_keywords:
        live_data = fetch_live_data(keyword)
        for article in live_data:
            published_at = article.get('publishedAt', datetime.datetime.utcnow())
            disaster_event = identify_disaster_event(article['title'])
            filtered_article = {
                'title': article['title'],
                'disaster_event': disaster_event,
                'timestamp': published_at,
                'source': article['source'],
                'url': article['url']
            }
            
            all_live_data.append(filtered_article)
    
    df = pd.DataFrame(all_live_data)

    df['disaster_event'].replace(to_replace="Unknown", value=np.nan, inplace=True)
    df.dropna(axis=0, inplace=True)
    df.drop_duplicates(subset='title', inplace=True)
    df['source'] = df['source'].apply(lambda x: x['name'])
    
    df['location_ner'] = df['title'].apply(extract_location_ner)
    
    df.dropna(axis=0, inplace=True)

    def fun(text):
        country, region, city = '', '', ''
        if len(text) == 1:
            country = text[0]
        elif len(text) == 2:
            country, region = text[0], text[1]
        elif len(text) == 3:
            country, region, city = text[0], text[1], text[2]
        return country, region, city

    a = df['location_ner'].apply(fun)

    df['Country'] = ''
    df['Region'] = ''
    df['City'] = ''

    df[['Country', 'Region', 'City']] = pd.DataFrame(a.tolist(), index=df.index)

    def create_location(row):
        if row['City']:
            return row['City']
        elif row['Region']:
            return row['Region']
        else:
            return row['Country']

    df['Location'] = df.apply(create_location, axis=1)
    df = df.dropna(subset=['Location'])

    
    df = df[~df['Location'].str.lower().isin(exclude_locations)]
    df = df[~df['url'].str.lower().str.contains('politics|yahoo|sports|entertainment|cricket')]

    df['Coordinates'] = df['Location'].apply(get_coordinates)

   

    df.drop('Coordinates', axis=1, inplace=True)

    df = df.dropna(subset=['Latitude', 'Longitude'])

    # MongoDB Atlas connection URI
    uri = "ENTER YOUR MONGODB ATLAS CONNECTION STRING"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Access the GeoNews database and disaster_info collection
    db = client["YOUR DATABASE NAME HERE"]
    collection = db["YOUR COLLECTION NAME HERE"]

    # Create a DataFrame

    # Convert DataFrame to a list of dictionaries
    data_list = df.to_dict(orient='records')

    # Insert the data list into the collection
    try:
        result = collection.insert_many(data_list)
        print("Documents inserted successfully. IDs:", result.inserted_ids)
    except Exception as e:
        print("An error occurred:", e)
