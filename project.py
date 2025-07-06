import streamlit as st
import requests
import csv
import pandas as pd
import time
import folium
from streamlit_folium import folium_static
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")

def log_weather_history(location, weather_data):
    with open("weather_history.txt", "a") as file:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"[{timestamp}] Weather in {location}: {weather_data}\n")

def weather_data(user_input):
    api_key = '6bd334abc9bfd21d79a7fe8b219a4b44'
    if not user_input:
        st.write("Please enter a city name.")
        return

    url = f'http://api.openweathermap.org/data/2.5/weather?q={user_input}&appid={api_key}'
    weather_data = requests.get(url)

    if weather_data.json().get('cod') == 404:
        st.write("No city found")
    else:
        weather_sys = weather_data.json()['weather'][0]['main']
        wind_speed = round(weather_data.json()['wind']['speed'] * (5 / 18))
        humidity = weather_data.json()['main']['humidity']
        temperature = weather_data.json()['main']['temp'] - 273.15
        feels_like = weather_data.json()['main']['feels_like'] - 273.15

        st.write(f"Weather in {user_input}: {weather_sys}")
        st.write(f"Wind speed in {user_input}: {wind_speed} km/h")
        st.write(f"Temperature in {user_input}: {temperature:.2f} °C")
        st.write(f"Humidity in {user_input}: {humidity}%")
        st.write(f"Fells like {feels_like:.2f} °C")

        log_weather_history(user_input, f"{weather_sys}, Wind speed: {wind_speed} km/h, Temperature: {temperature:.2f} °C, Humidity: {humidity}%, Feels like: {feels_like:.2f} °C")

def display_weather_history():
    st.title("Weather History")

    try:
        with open("weather_history.txt", "r") as file:
            weather_history = file.readlines()
            if weather_history:
                for entry in weather_history:
                    st.write(entry)
            else:
                st.write("No weather history available.")
    except FileNotFoundError:
        st.write("No weather history available.")

selected = option_menu(
    menu_title="SMART WEATHER NOTIFIER",
    options=["HOME", "DATA", "WEATHER", "HISTORY"],
    menu_icon=["home", 'home', 'home', 'home'],
    default_index=0,
    orientation="horizontal",
)

if selected == "HOME":
    pass
elif selected == "DATA":
    pass
elif selected == "WEATHER":
    pass
elif selected == "HISTORY":
    display_weather_history()


def long_lat(city):
    import requests
    import json

    api_url = 'https://api.api-ninjas.com/v1/geocoding?city={}'.format(city)
    headers = {'X-Api-Key': 'MzTYQ7JYCX8mAdO+8/k7IQ==3pyHgMBbcwSOCN3w'}
    response = requests.get(api_url, headers=headers)
    if response.status_code == requests.codes.ok:
        response = json.loads(response.text)
        lat = response[0]['latitude']
        long = response[0]['longitude']
        return lat, long
    else:
        print("Error:", response.status_code, response.text)

def clock_app():
    st.title("Clock")
    time_placeholder = st.empty()

    while True:
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime("%Y-%m-%d")
        current_day = time.strftime("%A")
        time_placeholder.text("Current Time: " + current_time + "\nDay: " + current_day + "\nDate: " + current_date)
        time.sleep(1)

def user_input():
    user_input = st.text_input("Get weather for City: ")
    if st.button("Get weather"):
        weather_data(user_input)
        to_long, to_lat = long_lat(user_input)

        m = folium.Map(location=[float(to_long), float(to_lat)], zoom_start=10)

        folium.Marker(location=[float(to_long), float(to_lat)], popup="London").add_to(m)

        with st.container():
            folium_static(m, width=500, height=350)

if selected == "HOME":
    clock_app()

if selected == "DATA":
    def add_person_in_excelfile(name, home, current, phone):
        try:
            df = pd.read_csv('Persons.csv')
        except FileNotFoundError:
            df = pd.DataFrame(columns=['Name', 'Home location', 'Current location', 'Phone number'])

        new_data = {"Name": name, "Home location": home, "Current location": current, "Phone number": phone}
        new_data_df = pd.DataFrame([new_data])
        updated_df = pd.concat([df, new_data_df])
        updated_df.to_csv('Persons.csv', index=False, columns=['Name', 'Home location', 'Current location', 'Phone number'])

    def remove_person_from_excelfile(name):
        try:
            df = pd.read_csv('Persons.csv')
        except FileNotFoundError:
            st.write("No 'Persons.csv' file found.")
            return

        updated_df = df[df['Name'] != name]
        updated_df.to_csv('Persons.csv', index=False, columns=['Name', 'Home location', 'Current location', 'Phone number'])
    
    def location_weather(name):
        try:
            df = pd.read_csv('Persons.csv')
        except FileNotFoundError:
            st.write("No 'Persons.csv' file found.")
            return
        except pd.errors.EmptyDataError:
            st.write("The CSV file is empty or has the wrong structure.")
            return
        
        row = df.loc[df['Name'] == name]
        if row.empty:
            st.write(f"No person found with the name {name}")
            return

        home_location = row['Home location'].values[0]
        current_location = row['Current location'].values[0]
        phone_number = row['Phone number'].values[0]

        home_weather_data = weather_data(home_location)
        current_weather_data = weather_data(current_location)

    try:
        df = pd.read_csv('Persons.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Name', 'Home location', 'Current location', 'Phone number'])

    st.write("Data from Excel file:")
    st.write(df)

    name_sel = st.text_input("Enter person name from above for fetching weather data of his home and current location: ")
    location_weather(name_sel)

    name = st.text_input("Enter a name: ")
    hl = st.text_input("Enter home location")
    Cl = st.text_input("Enter current location")
    ph = st.text_input("Enter Phone number")
    if st.button("Add person"):
        add_person_in_excelfile(name, hl, Cl, ph)

    remove_person = st.text_input("Enter the person name to remove")
    if st.button("Remove"):
        remove_person_from_excelfile(remove_person)


if selected == "WEATHER":
    user_input()

