import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# ——— Page config ———
st.set_page_config(
    page_title="🎵 Music Recommendation App",
    layout="wide"
)

# ——— Custom CSS ———
st.markdown("""
<style>
/* —— App background & text color —— */
[data-testid="stAppViewContainer"] {
    background-color: #121212 !important;
    color: #e0e0e0 !important;
}
/* —— Sidebar background —— */
[data-testid="stSidebar"] {
    background-color: #1f1f1f !important;
}
/* —— Headings —— */
h1 {
    font-size: 3rem !important;
    font-weight: 800 !important;
    color: #1DB954 !important;
    text-align: center;
}
h2, h3 {
    font-size: 1.5rem !important;
    font-weight: 600 !important;
    color: #1DB954 !important;
}
/* —— Button styling —— */
button {
    border: 2px solid #1DB954 !important;
    background-color: transparent !important;
    color: #1DB954 !important;
    padding: 0.5rem 1rem !important;
    border-radius: 8px !important;
}
button:hover {
    background-color: #1DB954 !important;
    color: #121212 !important;
}
/* —— Inputs & select boxes —— */
input, textarea, .stSelectbox > div, .stTextInput > div {
    background-color: #1f1f1f !important;
    color: #e0e0e0 !important;
}
/* —— Hide default Streamlit menu & footer —— */
#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

from dotenv import load_dotenv
import os

load_dotenv()  # reads .env into environment

SPOTIPY_CLIENT_ID     = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")


# ——— Spotify authentication ———
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET
))

# ——— Header ———
st.title("🎵 Music Recommendation App")
st.markdown(
    "<p style='text-align:center; color:gray;'>Search-based fallback: genre + decade (+ artist)</p>",
    unsafe_allow_html=True
)

# ——— Filters in the sidebar ———
with st.sidebar:
    st.header("🔎 Filters")
    moods   = ["Happy", "Sad", "Energetic", "Chill", "Romantic", "Focus"]
    genres  = ["pop","rock","classical","jazz","edm","hip-hop","r&b","country","metal"]
    decades = ["2020s","2010s","2000s","1990s","1980s","1970s"]

    mood   = st.selectbox("Mood", moods)
    genre  = st.selectbox("Genre", genres)
    decade = st.selectbox("Decade", decades)
    artist = st.text_input("Artist (optional)")

    st.markdown("---")
    get_recs = st.button("Get Recommendations")

# ——— Main content ———
if get_recs:
    # Map decade → year range
    decade_map = {
        "2020s": (2020,2023), "2010s": (2010,2019),
        "2000s": (2000,2009), "1990s": (1990,1999),
        "1980s": (1980,1989), "1970s": (1970,1979)
    }
    start_year, end_year = decade_map[decade]

    # Build search query
    query = f"genre:{genre} year:{start_year}-{end_year}"
    if artist:
        query += f" artist:{artist}"

    # Fetch tracks
    with st.spinner("Fetching tracks…"):
        results = sp.search(q=query, type="track", limit=50)
        tracks = results["tracks"]["items"][:10]

    # Display results
    if not tracks:
        st.info("No tracks found—try different filters.")
    else:
        st.subheader("Recommended Tracks")
        for t in tracks:
            name        = t["name"]
            artist_name = t["artists"][0]["name"]
            url         = t["external_urls"]["spotify"]
            album_img   = t["album"]["images"][0]["url"]
            preview     = t["preview_url"]

            cols = st.columns([1, 4])
            with cols[0]:
                st.image(album_img, width=100)
            with cols[1]:
                st.markdown(f"**[{name} – {artist_name}]({url})**")
                if preview:
                    st.audio(preview)
                else:
                    st.markdown("*No preview available.*")
            st.markdown("---")
