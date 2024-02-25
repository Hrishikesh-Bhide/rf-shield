import pandas as pd
import streamlit as st
from geopy.distance import geodesic
from streamlit_folium import folium_static
import folium
from geopy.geocoders import Nominatim
from resources.constants import tower_dataset, logo_path
from folium.plugins import Draw
import db
import google.generativeai as genai

def is_point_inside_circle(point_lat, point_lon, circle_lat, circle_lon, radius):
    # Calculate the distance between the point and the center of the circle
    distance = geodesic((point_lat, point_lon), (circle_lat, circle_lon)).meters
    return distance <= radius

def create_or_clear_file(filename):
            with open(filename, 'w'):  # Open file in write mode ('w')
                pass  # No need to write anything, just create or clear the file

filename = "./data/my_file.txt"
create_or_clear_file(filename)
print("File '{}' created or cleared.".format(filename))

def extract_state(address):
    us_states = {
        'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
        'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia',
        'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
        'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland',
        'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri',
        'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey',
        'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
        'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
        'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
        'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
    }
    
    #address = f"{location.address}, {location.city}, {location.state}, {location.postal_code}, {location.country}"
    address = str(address).title()  # Convert address to title case for case-insensitive comparison
    for state_name in us_states:
        if state_name in address:
            return state_name
    return None





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

        #st.write("Your Address: " + str(location))
        state = extract_state(location)
        print("State:", state)

        import requests
        import pandas as pd


        
        def remove_newlines_and_tabs(text):
            cleaned_text = text.replace('\n', '').replace('\t', '')
            return cleaned_text



        def search_news(query, location):
            api_key = ''

            base_url = 'https://api.serpwow.com/search'
            params = {
                'api_key': api_key,
                'q': f'news articles about cell phone tower installation in {location}',
                'engine': 'google',
                'google_domain': 'google.com',
                'num': 5,  # Number of results (max 10)
                'gl': 'us',  # Country code for search results
                'hl': 'en',  # Language code for search results
                'tbm': 'nws',  # Search type: news
            }

            response = requests.get(base_url, params=params)
            data = response.json()
            titles=[]
            urls=[]


            if 'organic_results' in data:
                for result in data['organic_results']:
                    title = result['title']
                    titles.append(title)
                    url = result['link']
                    urls.append(url)
                    data = {'Title': titles,'URL': urls}
                    
            else:
                print("No articles found.")
            return pd.DataFrame(data)

        news_df = search_news("news articles about cell phone tower installation", state)

        

        import requests
        from bs4 import BeautifulSoup
        import pandas as pd

        # Function to remove newlines and tabs from text
        # def remove_newlines_and_tabs(text):
        #     cleaned_text = text.replace('\n', '').replace('\t', '')
        #     return cleaned_text

        # Assuming you already have a DataFrame named df with a column 'URL' containing URLs

        for url in news_df['URL']:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                article = soup.find('article')
                if article:
                    article_content = article.get_text(strip=True)  # Extract article content without newlines and tabs
                    cleaned_text = remove_newlines_and_tabs(article_content)
                    with open("./data/my_file.txt", 'a', encoding='utf-8') as file:
                        file.write(cleaned_text + '\n\n')  # Save article content to a document
                        print("written successfully")
                else:
                    print(f"No article content found on {url}")
            else:
                print(f"Failed to fetch URL: {url}")


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
            st.markdown("<h3 style='text-align: center; color: green; font-size: 24px;'>RF-Shielded Area</h3>",
                        unsafe_allow_html=True)
        else:
            st.markdown("<h3 style='text-align: center; color: red; font-size: 24px;'>RF-Exposed Area</h3>",
                        unsafe_allow_html=True)
        folium_static(mymap)


        def to_markdown(text):
            lines = text.split('\n')
            return lines



        # Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
        GOOGLE_API_KEY= ''

        genai.configure(api_key=GOOGLE_API_KEY)
            
        model = genai.GenerativeModel('gemini-pro')


        with open('./data/my_file.txt', 'r', encoding='utf-8') as file:
            content = file.read()  # Read the entire content of the file
            
        prompt = f"You are given content of news articles and you have to summarise the {content} in one single paragraph. I need paragraph as output only."
        response = model.generate_content(prompt)
        st.subheader("Trending news around your place:")
        st.write(response.text)

        st.write("For more information please refer below news articles: ", unsafe_allow_html=True)
        for index, row in news_df.iterrows():
            st.write(f"{index + 1}. [{row['Title']}]({row['URL']})")
