import streamlit as st

st.title(" Trending Bollywood Movies")

movies = [
    {
        "title": "Pathaan",
        "poster": "https://upload.wikimedia.org/wikipedia/en/1/1c/Pathaan_film_poster.jpg",
        "description": "A high-octane action thriller starring Shah Rukh Khan as a RAW agent."
    },
    {
        "title": "Jawan",
        "poster": "https://upload.wikimedia.org/wikipedia/en/b/b5/Jawan_poster.jpg",
        "description": "An action drama exploring social issues through a gripping vigilante story."
    },
    {
        "title": "Animal",
        "poster": "https://upload.wikimedia.org/wikipedia/en/c/c9/Animal_2023_film_poster.jpg",
        "description": "An intense family drama centered on a son's complicated relationship with his father."
    },
    {
        "title": "12th Fail",
        "poster": "https://upload.wikimedia.org/wikipedia/en/e/e6/12th_Fail_poster.jpg",
        "description": "An inspiring true story of perseverance to crack the UPSC exam."
    },
    {
        "title": "Stree 2",
        "poster": "https://upload.wikimedia.org/wikipedia/en/6/6e/Stree_2_poster.jpg",
        "description": "A horror-comedy sequel following the town's battle against a new supernatural threat."
    }
]

for movie in movies:
    st.subheader(movie["title"])
    st.image(movie["poster"], width=200)
    st.write(movie["description"])
   