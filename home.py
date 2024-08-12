import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import plotly.express as px
from wordcloud import WordCloud
from datetime import datetime, timedelta, timezone
from pymongo import MongoClient

def main():
    # MongoDB Atlas connection URI
    uri =  "mongodb+srv://aryanrvimpadapu:MUTBZgApDRVxxIXY@cluster0.fs4he7a.mongodb.net/?retryWrites=true&w=majority"
    

    # Create a new client and connect to the server
    client = MongoClient(uri)

    # Access the GeoNews database and disaster_info collection
    db = client["GeoNews"]
    collection = db["disaster_info"]

    # Convert MongoDB cursor to DataFrame
    df = pd.DataFrame(list(collection.find()))
    df.drop_duplicates(subset='title', inplace=True)
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['Latitude', 'Longitude'])
    exclude_locations = ['avalanche', 'blizzard', 'cyclone', 'drought', 'earthquake', 
                        'flood', 'heatwave', 'hurricane', 'landslide', 'storm', 
                        'tornado', 'tsunami', 'volcano', 'wildfire','hockey','a.i.','netflix']

    # Filter the DataFrame to exclude the locations in the exclude_locations list
    df = df[~df['Location'].str.lower().isin(exclude_locations)]
    df = df[~df['url'].str.lower().str.contains('politics|yahoo|sports')]
    df = df[~df['title'].str.lower().str.contains('tool|angry')]

    df['date_only'] = df['timestamp'].dt.strftime('%Y-%m-%d')

    # Drop duplicate rows based on the combination of date_only, disaster_event, and Location
    df.drop_duplicates(subset=['date_only', 'disaster_event', 'Location'], inplace=True)
    df.drop(columns=['date_only'], inplace=True)



    # Disaster event filter at the center
    st.title("Geospatial Visualization for Disaster Monitoring")
    selected_events = st.multiselect("Select Disaster Events", ["All"] + list(df["disaster_event"].unique()), default=["All"])

    # Sidebar widgets for filtering
    st.sidebar.header('Filter Data')

    # Start date filter
    start_date_min = datetime.utcnow().date() - timedelta(days=7)  # 6 days before the end date
    start_date_past = datetime(2023, 1, 1)  # Assuming the data starts from the year 2000, change accordingly
    start_date = st.sidebar.date_input("Start date", start_date_min, min_value=start_date_past,
                                    max_value=datetime.utcnow().date())

    # End date filter
    end_date = st.sidebar.date_input("End date", datetime.utcnow().date(), min_value=start_date_past, max_value=datetime.utcnow().date())

    # Convert Streamlit date inputs to timezone-aware datetime objects with UTC timezone
    start_date_utc = datetime.combine(start_date, datetime.min.time()).replace(tzinfo=timezone.utc)
    end_date_utc = datetime.combine(end_date, datetime.max.time()).replace(tzinfo=timezone.utc)

    # Filter dataframe based on selected filters
    if "All" in selected_events:
        filtered_df = df[(df['timestamp'] >= start_date_utc) & (df['timestamp'] <= end_date_utc)]
    else:
        filtered_df = df[(df['timestamp'] >= start_date_utc) & (df['timestamp'] <= end_date_utc) & (
                df['disaster_event'].isin(selected_events))]

    # Check if filtered_df is empty after filtering
    if filtered_df.empty:
        st.subheader(":green[No Disaster data available after filtering based on the condition]")
    else:
        map_center = (filtered_df['Latitude'].mean(), filtered_df['Longitude'].mean())
        mymap = folium.Map(location=map_center, zoom_start=4, fullscreen_control=True)

        # Create a MarkerCluster object
        marker_cluster = MarkerCluster().add_to(mymap)

        # Function to determine custom icon path based on disaster event
        def get_custom_icon_path(disaster_event):
            icon_paths = {
                "Avalanche": 'https://cdn-icons-png.flaticon.com/128/3496/3496600.png',
                "Blizzard": 'https://cdn-icons-png.flaticon.com/128/1781/1781928.png',
                "Cyclone": 'https://cdn-icons-png.flaticon.com/128/10159/10159051.png',
                "Drought": 'https://cdn-icons-png.flaticon.com/128/7858/7858410.png',
                "Earthquake": 'https://icons.iconarchive.com/icons/icons8/windows-8/512/Weather-Earthquakes-icon.png',
                "Flood": 'https://cdn4.iconfinder.com/data/icons/eldorado-weather/40/flood-512.png',
                "Heatwave": 'https://cdn-icons-png.flaticon.com/128/7110/7110118.png',
                "Hurricane": 'https://cdn-icons-png.flaticon.com/128/798/798326.png',
                "Landslide": 'https://cdn-icons-png.flaticon.com/128/3496/3496896.png',
                "Storm": 'https://cdn-icons-png.flaticon.com/128/8048/8048062.png',
                "Tornado": 'https://cdn-icons-png.flaticon.com/128/7251/7251087.png',
                "Tsunami": 'https://cdn-icons-png.flaticon.com/128/2856/2856848.png',
                "Volcano": 'https://cdn-icons-png.flaticon.com/128/7265/7265026.png',
                "Wildfire": 'https://cdn-icons-png.flaticon.com/128/2321/2321741.png',
            }
            return icon_paths.get(disaster_event, 'https://cdn-icons-png.flaticon.com/128/4357/4357606.png')

        # Add markers to the MarkerCluster object
        for index, row in filtered_df.iterrows():
            custom_icon_path = get_custom_icon_path(row['disaster_event'])
            custom_icon = folium.CustomIcon(
                icon_image=custom_icon_path,
                icon_size=(35, 35),
                icon_anchor=(15, 30),
                popup_anchor=(0, -25)
            )
            popup_content = f"<a href='{row['url']}' target='_blank'>{row['title']}</a>"
            tooltip_content = f"{row['disaster_event']}, {row['Location']}"
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=folium.Popup(popup_content, max_width=300),
                icon=custom_icon,
                tooltip=tooltip_content
            ).add_to(marker_cluster)

        # Map style options
        base_map_styles = {
            'Terrain': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Physical_Map/MapServer/tile/{z}/{y}/{x}',
            'Satellite': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            'Ocean': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}',
            'Detail': 'https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}'
        }

        # Add base map styles as layers
        for name, url in base_map_styles.items():
            folium.TileLayer(url, attr="Dummy Attribution", name=name).add_to(mymap)

        # Add layer control to the map with collapsed=True to hide the additional layers
        folium.LayerControl(collapsed=True).add_to(mymap)

        # Display the Folium map in Streamlit
        st_folium(mymap, width='100%', height=620)

        # Display filtered data
        with st.expander(f"Disaster Data Overview"):
            expander_title = f"### Disaster Data for {'All Events' if 'All' in selected_events else ', '.join(selected_events)}"
            st.markdown(expander_title, unsafe_allow_html=True)

            columns_to_display = ['title', 'disaster_event', 'timestamp', 'source', 'url', 'Location']
            st.write(filtered_df[columns_to_display])

    # Assuming df_filtered is already defined as per your instructions
    df_filtered = df[df['disaster_event'].isin(["Earthquake", "Flood", "Cyclone", "Volcano"])]

    # Filter recent events from the past 7 days
    seven_days_ago = pd.Timestamp(datetime.utcnow() - timedelta(days=5), tz="UTC")
    filtered_recent_events = df_filtered[df_filtered['timestamp'] >= seven_days_ago]

    # Sort filtered recent events by timestamp in descending order
    filtered_recent_events_sorted = filtered_recent_events.sort_values(by='timestamp', ascending=False)

    # Create marquee content
    marquee_content = ""
    for index, row in filtered_recent_events_sorted.iterrows():
        marquee_content += f"<a href='{row['url']}' target='_blank'>{row['title']}</a> <br><br>"

    # Define the HTML, CSS, and JavaScript for the marquee
    marquee_html = f"""
        <h1>Key Events</h1>
        <div class="marquee-container" onmouseover="stopMarquee()" onmouseout="startMarquee()">
            <div class="marquee-content">{marquee_content}</div>
        </div>
        <style>
            .marquee-container {{
                height: 100%; /* Set the height to occupy the entire sidebar */
                overflow: hidden;
            }}
            .marquee-content {{
                animation: marquee 40s linear infinite;
            }}
            @keyframes marquee {{
                0%   {{ transform: translateY(10%); }}
                100% {{ transform: translateY(-100%); }}
            }}
            .marquee-content:hover {{
                animation-play-state: paused;
            }}
        </style>
        <script>
            function stopMarquee() {{
                document.querySelector('.marquee-content').style.animationPlayState = 'paused';
            }}
            function startMarquee() {{
                document.querySelector('.marquee-content').style.animationPlayState = 'running';
            }}
        </script>
    """

    # Render the marquee in the sidebar with Streamlit
    st.sidebar.markdown(marquee_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    st.set_page_config(layout="wide")
