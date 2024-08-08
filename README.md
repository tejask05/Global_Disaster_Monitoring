
# GeoNews: Real Time Geospatial Disaster Monitoring Visualization

This project provides an interactive web application for visualizing geospatial data related to various disaster events. It utilizes data from the GeoNews database and allows users to filter and explore disaster events based on different criteria such as event type, date range, and location.


## Project URL

The project can be viewed at [global-disaster-monitoring.streamlit.app](https://global-disaster-monitoring.streamlit.app).

## Features

- **Interactive Map Visualization**: View the geographical distribution of disaster events on an interactive map powered by Folium.
- **Filtering Options**: Filter disaster events based on event type and date range using Streamlit sidebar widgets.
- **Insights and Analytics**: Gain insights into disaster events through various interactive visualizations including charts, word clouds, and event counts over time.
- **Key Events Marquee**: Display a scrolling marquee in the sidebar showcasing recent key events with clickable links to more information.
- **Dynamic Updates**: The application dynamically updates visualizations and data based on user-selected filters.

## Disaster News Data Extraction and MongoDB Insertion

This newapi script fetches live disaster-related news articles from the News API, extracts relevant information such as title, publication timestamp, source, and location, and inserts it into a MongoDB database for further analysis and visualization.

### Functionality

- **Live Data Retrieval**: Utilizes the News API to fetch recent news articles related to various disaster events such as earthquakes, floods, hurricanes, etc.
- **Data Filtering**: Filters out irrelevant articles and identifies the type of disaster event based on predefined keywords.
- **Named Entity Recognition (NER)**: Uses spaCy to extract location entities (e.g., countries, regions, cities) from the article titles.
- **Geocoding**: Converts extracted location names into geographical coordinates (latitude and longitude) using the Geopy library.
- **Data Cleaning**: Removes duplicates, excludes irrelevant locations and URLs, and handles missing values.
- **MongoDB Insertion**: Inserts the cleaned and processed data into a MongoDB Atlas database collection.

## Usage

1. Clone the repository to your local machine.
2. Make sure you have installed all required Python dependencies listed in the `requirements.txt`.
3. Obtain a News API key and set it as `NEWSAPI_KEY` variable.
4. Update the `exclude_locations` list to exclude any additional irrelevant locations.
5. Run the script `datacollection.py`. It will fetch live data, process it, and insert it into your `MongoDB database`.
6. Set up a MongoDB Atlas account and configure the connection URI in the `newsapi.py` file.
7. Run the Streamlit application using the command `streamlit run geonews.py`.
8. Access the application in your web browser at the provided URL.

### MongoDB Configuration

- MongoDB Atlas URI: Replace `"YOUR_MONGODB_URI"` in the script with your actual MongoDB Atlas connection URI.
- Database Name: The script assumes a database named `"GeoNews"` is available in your MongoDB Atlas cluster. You can change this as needed.
- Collection Name: The script inserts data into a collection named `"disaster_info"`. Modify this collection name if required.

### Note

Ensure that your MongoDB Atlas cluster is properly configured to accept incoming connections from your Python script. Additionally, make sure your News API key is valid and has sufficient permissions to access news articles.


## Technologies Used

- Python
- Pandas
- Folium
- Streamlit
- Plotly
- Seaborn
- WordCloud
- MongoDB

## Example Video For Disaster Monitoring

https://github.com/user-attachments/assets/4f75711c-5315-499b-bc76-1e87ef8165fb


https://github.com/user-attachments/assets/325df90a-90dd-421a-bf77-65b9c95a2b67






## Contributing

Contributions are welcome! Feel free to open issues or pull requests for any improvements or bug fixes.

