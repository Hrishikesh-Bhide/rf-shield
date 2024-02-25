import psycopg2
import pandas as pd
import resources.constants

def dms_to_decimal(degrees, minutes, seconds):
    decimal_degrees = degrees + (minutes / 60) + (seconds / 3600)
    return decimal_degrees

def connect_to_database(conn_str):
    try:
        # Create a new database session
        conn = psycopg2.connect(conn_str)
        return conn
    except Exception as e:
        print(f"Unable to connect to the database: {e}")
        return None


def create_tables(cur, conn):
    try:
        # Test Query
        cur.execute("CREATE TABLE Tower_Location(tower_id INT PRIMARY KEY, Lat FLOAT, Lng FLOAT, Color text)")
        conn.commit()
        print("Table created")
    except Exception as e:
        print(f"An error occurred while creating tables: {e}")


def insert_data(cur, conn):
    tower_dataset = pd.read_csv(resources.constants.tower_dataset)
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
        lng_decimal.append(-longitude_decimal)

    try:
        i = 0
        for start_lat, start_lng in zip(lat_decimal, lng_decimal):
            color = "'red'"
            cur.execute(
                f"INSERT INTO Tower_Location(tower_id, Lat, Lng, Color) VALUES ({i + 1}, {start_lat}, {start_lng}, {color})")
            i += 1

        print("Data inserted successfully.")
        conn.commit()
    except Exception as e:
        print(f"An error occurred during data insertion: {e}")


def get_tower_data_from_database(cur):
    try:
        cur.execute("SELECT Lat, Lng, Color FROM Tower_Location")
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Error retrieving accident data: {e}")
        return []
