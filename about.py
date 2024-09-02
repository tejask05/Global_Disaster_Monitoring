import streamlit as st

def main():
    st.header("Geo-Spatial Visualization for Disaster Monitoring")
    st.write(
        """
        Geo-Spatial Visualization for Disaster Monitoring is a web application to monitor and visualize disasters in real-time through the analysis of news articles. By extracting valuable information from news sources, the project aims to provide a comprehensive overview of ongoing and past disaster events. 
        """
    )

    st.subheader("Features")
    st.markdown("""
    1. Interactive Map Visualization: View the geographical distribution of disaster events on an interactive map powered by Folium.
    2. Filtering Options: Filter disaster events based on event type and date range using Streamlit sidebar widgets.
    3. Insights and Analytics: Gain insights into disaster events through various interactive visualizations including charts, word clouds, and event counts over time.
    4. Key Events Marquee: Display a scrolling marquee in the sidebar showcasing recent key events with clickable links to more information.
    5. Dynamic Updates: The application dynamically updates visualizations and data based on user-selected filters.
    """)

    st.subheader("Data Sources")
    st.write(
        """
        The project primarily collects data from NewsAPI, a service providing access to various news articles.
        After preprocessing, the data is stored in MongoDB with the database name GeoNews. 
        Additional data sources may be integrated to enhance the coverage and accuracy of the information.
        """
    )

    st.subheader("Technologies Used")
    st.write(
        """
        1. **Python**: Programming language for data processing and visualization.
        2. **Streamlit**: Framework for building interactive web applications.
        3. **Pandas**: Library for data manipulation and analysis.
        4. **Folium**: Library for creating interactive maps.
        5. **Plotly**: Library for generating interactive plots and charts.
        6. **MongoDB**: Database for storing and querying geospatial data.
        """
    )

    st.subheader("GitHub Repository")
    st.write("[Link to GitHub](https://github.com/ARYANRVIMPADAPU/GeoNews)")



