import streamlit as st
st.set_page_config(
    page_title="BHASHAUNVEILED",
    page_icon=":material/library_books:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

home_page = st.Page("Home.py", title="Home", icon=":material/home:")
univ_page = st.Page("University.py", title="Academic institutions ", icon=":material/things_to_do:")
year_comp_page = st.Page("prev_year_comp.py", title="Previous Year Comparison ", icon=":material/things_to_do:")

pg = st.navigation([home_page, univ_page, year_comp_page])
pg.run()