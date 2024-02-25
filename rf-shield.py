import pandas as pd
import streamlit as st
from geopy.distance import geodesic
from streamlit_folium import folium_static
import folium
from geopy.geocoders import Nominatim
from resources.constants import tower_dataset, logo_path
from folium.plugins import Draw
import db

def is_point_inside_circle(point_lat, point_lon, circle_lat, circle_lon, radius):
    # Calculate the distance between the point and the center of the circle
    distance = geodesic((point_lat, point_lon), (circle_lat, circle_lon)).meters
    return distance <= radius


if __name__ == '__main__':
    conn_str = 'postgresql://postgres:ZTcdErRGGp7THlrW@org-zenith-inst-rf-shield.data-1.use1.tembo.io:5432/postgres'
    conn = db.connect_to_database(conn_str)
    if conn:
        tower_data = []
        try:
            cur = conn.cursor()
            #db.create_tables(cur, conn)
            #db.insert_data(cur, conn)
            tower_data = db.get_tower_data_from_database(cur)
            cur.close()
            conn.close()
        except Exception as e:
            st.error(f"An error occurred: {e}")


    with st.sidebar:
        st.markdown("<h1 style='text-align: center; color: blue;font-size: 30px;'>RF Shield</h1>",
                    unsafe_allow_html=True)
        st.image(logo_path, width=250)
        src = st.text_input("**Enter Address To Check Safety**")

        find_house_safety = st.button("**Check Your Safety**")

    if find_house_safety == True:
        geolocator = Nominatim(user_agent="my_streamlit_app")
        location = geolocator.geocode(src)
        st.subheader(str(location))

        flag = False
        radius_color = "blue"
        radius = 400
        for row in tower_data:
            is_inside = is_point_inside_circle(location.latitude, location.longitude, row[0], row[1], radius)
            if is_inside == True:
                flag = True
                radius_color = "red"
                break

        mymap1 = folium.Map(location=[location.latitude, location.longitude])

        # add marker for Liberty Bell
        tooltip = location
        folium.Marker([location.latitude, location.longitude], popup="Liberty Bell", tooltip=tooltip).add_to(mymap1)

        df = pd.DataFrame(tower_data, columns=["LATITUDE", "LONGITUDE", "Color"])

        # Add scatter plot markers to the map using the latitude and longitude from the DataFrame
        for _, row in df.iterrows():
            folium.CircleMarker(location=[row['LATITUDE'], row['LONGITUDE']],
                                radius=5,  # Adjust the radius as needed
                                color=row['Color'],
                                fill=True).add_to(mymap1)
        # folium_static(mymap1)


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
        # folium_static(mymap)

        folium_static(mymap1)
        if flag == False:
            st.markdown("<h3 style='text-align: center; color: green; font-size: 24px;'>This is Safe Area</h3>", unsafe_allow_html=True)
        else:
            st.markdown("<h3 style='text-align: center; color: red; font-size: 24px;'>This is not Safe Area</h3>", unsafe_allow_html=True)
        folium_static(mymap)
