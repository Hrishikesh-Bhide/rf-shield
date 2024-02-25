import pandas as pd
import streamlit as st
from geopy.distance import geodesic
from streamlit_folium import folium_static
import folium
from geopy.geocoders import Nominatim
from resources.constants import tower_dataset, logo_path
from folium.plugins import Draw


def dms_to_decimal(degrees, minutes, seconds):
    decimal_degrees = degrees + (minutes / 60) + (seconds / 3600)
    return decimal_degrees


def is_point_inside_circle(point_lat, point_lon, circle_lat, circle_lon, radius):
    # Calculate the distance between the point and the center of the circle
    distance = geodesic((point_lat, point_lon), (circle_lat, circle_lon)).meters
    # st.write(distance)
    # st.write(radius)
    # st.write(point_lat)
    # st.write(point_lon)
    # st.write("--------")
    # Check if the distance is less than or equal to the radius
    return distance <= radius


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
        st.markdown("<h1 style='text-align: center; color: blue;font-size: 30px;'>RF Shield</h1>",
                    unsafe_allow_html=True)
        st.image(logo_path, width=250)
        # Centered image with custom CSS
        src = st.text_input("**Enter Address To Check Safety**")

        find_house_safety = st.button("**Check Your Safety**")

    if find_house_safety == True:
        geolocator = Nominatim(user_agent="my_streamlit_app")
        location = geolocator.geocode(src)
        st.subheader(str(location))

        flag = False
        radius_color = "blue"
        radius = 400
        for row in combined_coordinates:
            is_inside = is_point_inside_circle(location.latitude, location.longitude, row[0], row[1], radius)
            if is_inside == True:
                flag = True
                radius_color = "red"
                break

        mymap = folium.Map(location=[location.latitude, location.longitude], zoom_start=15)

        # add marker for Liberty Bell
        tooltip = location
        folium.Marker([location.latitude, location.longitude], popup="Liberty Bell", tooltip=tooltip).add_to(mymap)

        # Add scatter plot markers to the map using the latitude and longitude from the DataFrame
        for _, row in df.iterrows():
            folium.CircleMarker(location=[row['LATITUDE'], row['LONGITUDE']],
                                radius=5,  # Adjust the radius as needed
                                color=row['Color'],
                                fill=True).add_to(mymap)

        radius = 400
        folium.Circle(
            location=[location.latitude, location.longitude],
            radius=radius,
            color=radius_color,
            fill=True,
            fill_color='blue',
            fill_opacity=0.2
        ).add_to(mymap)
        folium_static(mymap)

        if flag == False:
            st.markdown("<h3 style='text-align: center;'>This is Safe Area</h3>", unsafe_allow_html=True)
        else:
            st.markdown("<h3 style='text-align: center;'>This is not Safe Area</h3>", unsafe_allow_html=True)
