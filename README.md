# Smart Weather Notifier
This is a Streamlit-based Python project that serves as a smart weather dashboard with additional utilities.

It allows you to:

Check live weather by city name.

Store and view weather history.

Track multiple persons' home & current locations and their weather.

Visualize weather locations on a map.

See a live clock.

# Features

1.) HOME

Shows a live digital clock with day and date.


2.) DATA

Manage persons' data (name, home location, current location, phone).

Save to Persons.csv.

Remove persons.

Get weather data for their home & current location.


3.) WEATHER

Get live weather by entering any city.

See weather info on an interactive Folium map.
Logs history in weather_history.txt.


4.) HISTORY

View all previous weather queries from weather_history.txt.

# Install dependencies

Make sure you have Python 3.8+ installed.

pip install streamlit, pandas, folium, streamlit-folium, streamlit-option-menu, requests

# Run the app

Run this command in your project directory:

streamlit run project.py
