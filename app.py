import streamlit as st
import requests

# Page Config (layout="wide" rakhvathi title ek j line ma aavse)
st.set_page_config(page_title="Movie Recommender", page_icon="🍿", layout="wide")

# Title ne ek j line ma rakhva mate HTML no use
st.markdown("<h1 style='text-align: center; white-space: nowrap;'>🍿 Movie Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("---")

# Search Box
movie_name = st.text_input("Enter a Movie you like (e.g., Jawan, Baahubali, Kalki):", placeholder="Enter movie name...")

# Center Button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    search_button = st.button("🔍 Get Recommendations", use_container_width=True)

if search_button:
    if movie_name:
        with st.spinner('Fetching movies from Graph Database... ⏳'):
            try:
                # Backend API Call
                response = requests.get(f"http://localhost:8000/recommend/{movie_name}")
                if response.status_code == 200:
                    data = response.json()
                    
                    if "message" in data:
                        st.warning(f"⚠️ {data['message']}")
                    else:
                        st.success(f"🎬 Users who liked **{data['movie'].upper()}** also liked:")
                        
                        for idx, rec in enumerate(data['recommendations']):
                            st.info(f"**{idx + 1}. {rec['title']}** (Match Score: {rec['score']})")
                else:
                    st.error(f"❌ Backend Database Error: {response.text}")
            except Exception as e:
                st.error("❌ Backend is not running! Please ensure your FastAPI server is running.")
    else:
        st.warning("⚠ Please enter a movie name first.")