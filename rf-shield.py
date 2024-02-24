import pandas as pd
import streamlit as st
from geopy.distance import geodesic
from streamlit_folium import folium_static
import folium
from geopy.geocoders import Nominatim
from resources.constants import tower_dataset
from folium.plugins import Draw


def dms_to_decimal(degrees, minutes, seconds):
    decimal_degrees = degrees + (minutes / 60) + (seconds / 3600)
    return decimal_degrees


if __name__ == '__main__':

    tower_dataset = pd.read_csv(tower_dataset)
    lats = tower_dataset['LAT_DMS']
    lngs = tower_dataset['LON_DMS']
    lat_decimal = []
    lng_decimal = []
    for lat in lats:
        lat_arr = lat.split(",")
        latitude_decimal = dms_to_decimal(int(lat_arr[0]), int(lat_arr[1]), int(lat_arr[2]))
        lat_decimal.append(latitude_decimal)

    for lng in lngs:
        lng_arr = lng.split(",")
        longitude_decimal = dms_to_decimal(int(lng_arr[0]), int(lng_arr[1]), int(lng_arr[2]))
        lng_decimal.append(longitude_decimal)

    combined_coordinates = []
    color = []
    for lat, lng in zip(lat_decimal, lng_decimal):
        combined_coordinates.append((lat, -lng))
        color.append('#FF0000')

    df = pd.DataFrame(combined_coordinates, columns=["LATITUDE", "LONGITUDE"])
    df['Color'] = color

    with st.sidebar:
        st.markdown("<h1 style='text-align: center; color: blue;font-size: 30px;'>Safe House</h1>",
                    unsafe_allow_html=True)
        # st.image(logo_path, width=250)
        # Centered image with custom CSS
        src = st.text_input("Enter Hourse Address To Check Safety")

        find_house_safety = st.button("Check Your Home Safety")

    if find_house_safety == True:
        geolocator = Nominatim(user_agent="my_streamlit_app")
        location = geolocator.geocode(src)
        st.write("Your Address: " + str(location))

        mymap = folium.Map(location=[location.latitude, location.longitude])

        # add marker for Liberty Bell
        tooltip = location
        folium.Marker([location.latitude, location.longitude], popup="Liberty Bell", tooltip=tooltip).add_to(mymap)

        
        