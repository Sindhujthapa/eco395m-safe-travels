from pathlib import Path
import streamlit as st
import psycopg2
import os
import requests
from dotenv import load_dotenv
from PIL import Image

st.markdown(
    """
    <style>
    .title {
        text-align: center;
        font-family: 'Comic Sans MS', cursive, sans-serif;
        font-size: 3em;
        color: #4A772F;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="title">🥒🎾PickleSpots🎾🥒</div>', unsafe_allow_html=True)
st.text(
    "This is an app designed to recommend a nearby pickleball court and corresponding outfit suggestions for any vacationer traveling to a destination of the top 50 most-visited cities in the United States. This recommendation will be based on proximity, weather, and the number of courts available at the nearby places."
)
load_dotenv()

try:
    DATABASE_HOST = os.environ["DATABASE_HOST"]
    DATABASE_DATABASE = os.environ["DATABASE_DATABASE"]
    DATABASE_USERNAME = os.environ["DATABASE_USERNAME"]
    DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"]
    DATABASE_PORT = os.environ["DATABASE_PORT"]
except KeyError as e:
    st.error(f"Missing environment variable: {e}")
    st.stop()


def create_connection():
    try:
        conn = psycopg2.connect(
            host=DATABASE_HOST,
            database=DATABASE_DATABASE,
            user=DATABASE_USERNAME,
            password=DATABASE_PASSWORD,
            port=DATABASE_PORT,
        )
        return conn
    except psycopg2.Error as e:
        st.error(f"Database connection error: {e}")
        st.stop()


def get_available_cities():
    conn = create_connection()
    cursor = conn.cursor()
    query = """SELECT DISTINCT ci."Name" FROM "City" ci ORDER BY ci."Name" ASC"""
    cursor.execute(query)
    cities = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return cities


def get_courts_by_city_and_number(city_name, min_courts):
    conn = create_connection()
    cursor = conn.cursor()

    if min_courts is None:
        query = """
        SELECT c."Name", c."NumberOfCourts", c."Lines", c."Nets"
        FROM "Courts" c
        JOIN "City" ci ON c."CityId" = ci."CityId"
        WHERE ci."Name" = %s
        """
        cursor.execute(query, (city_name,))
    else:
        query = """
        SELECT c."Name", c."NumberOfCourts", c."Lines", c."Nets"
        FROM "Courts" c
        JOIN "City" ci ON c."CityId" = ci."CityId"
        WHERE ci."Name" = %s AND c."NumberOfCourts" >= %s
        """
        cursor.execute(query, (city_name, min_courts))

    courts = cursor.fetchall()
    cursor.close()
    conn.close()
    return courts


def get_google_maps_photo(court_name, city_name, api_key):
    search_query = f"{court_name} {city_name}"
    search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    search_params = {"query": search_query, "key": api_key}

    response = requests.get(search_url, params=search_params)
    if response.status_code == 200:
        results = response.json().get("results")
        if results:
            place_id = results[0].get("place_id")
            photo_reference = results[0].get("photos", [{}])[0].get("photo_reference")
            if photo_reference:
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo"
                photo_params = {
                    "maxheight": 200,
                    "maxwidth": 200,
                    "photoreference": photo_reference,
                    "key": api_key,
                }
                return f"{photo_url}?maxwidth=400&photoreference={photo_reference}&key={api_key}"
    return None


def main():
    try:
        image_path = Path("pickleball_stock_image.jpg")
        image = Image.open(image_path)
        st.image(image, width=1000)
    except FileNotFoundError:
        st.warning(
            "Image file not found. Please ensure the file is in the working directory."
        )

    st.title("Pickleball Court Finder")
    st.markdown(
        "Find pickleball courts in your city and receive advice on what to wear based on the weather!"
    )

    # Dropdown for city selection
    cities = get_available_cities()
    city_name = st.selectbox("Select your city", options=["Select city"] + cities)

    # Dropdown for number of courts
    court_options = ["Any"] + list(range(1, 6))
    selected_court_option = st.selectbox(
        "Select the minimum number of courts", options=court_options, index=0
    )

    min_courts = None if selected_court_option == "Any" else selected_court_option

    if city_name:
        courts = get_courts_by_city_and_number(city_name, min_courts)

        if courts:
            st.subheader(
                f"Court Information for {city_name}:"
                + (f" (Minimum {min_courts} courts)" if min_courts else "")
            )
            for court in courts:
                court_name = court[0]
                court_query = f"{court_name} {city_name}".replace(" ", "+")
                google_maps_link = (
                    f"https://www.google.com/maps/search/?api=1&query={court_query}"
                )

                col1, col2 = st.columns([3, 2])

                with col1:
                    st.markdown(
                        f"[**{court_name}**]({google_maps_link})",
                        unsafe_allow_html=True,
                    )
                    st.write(f"**Number of Courts**: {court[1]}")
                    st.write(f"**Lines**: {court[2]}")
                    st.write(f"**Nets**: {court[3]}")

                with col2:
                    photo_url = get_google_maps_photo(
                        court_name, city_name, os.environ["MAPS_API_KEY"]
                    )
                    if photo_url:
                        st.image(photo_url, width=200)
                    else:
                        st.write("No photo available.")

                st.write("---")
        else:
            st.write(
                f"No court information found for {city_name}."
                + (f" with at least {min_courts} courts." if min_courts else "")
            )

    st.markdown("---")
    st.markdown("Data collected from pickleheads.com")
    st.markdown("Images taken from Google's Places API")
    st.markdown(
        "Project created by Divya, Danny, Jisoo, Juan, Nick, and Sindhuj for ECO395M"
    )


if __name__ == "__main__":
    main()
