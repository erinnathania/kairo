import streamlit as st
from pages.home import show_home
from pages.mindfulness import show_mindfulness
from pages.journal import show_journal
from pages.habits import show_habits
from pages.summary import show_summary
from pages.profile import show_profile
from pages.badges_page import show_badges
from pages.pet_page import show_pet

st.set_page_config(page_title="Kairo", page_icon=None, layout="wide")

# Initialize page state
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Sidebar — settings and profile only
with st.sidebar:
    st.title("Kairo")
    st.divider()
    if st.button("Profile", use_container_width=True):
        st.session_state.page = "Profile"
        st.rerun()
    if st.button("Settings", use_container_width=True):
        st.session_state.page = "Settings"
        st.rerun()
    st.divider()
    if st.button("Back to Home", use_container_width=True):
        st.session_state.page = "Home"
        st.rerun()
    st.caption("CWB Hackathon 2026")

# Route to the correct page
page = st.session_state.page

if page == "Home":
    show_home()
elif page == "Mind":
    show_mindfulness()
elif page == "Journal":
    show_journal()
elif page == "Habits":
    show_habits()
elif page == "Daily Summary":
    show_summary()
elif page == "Badges":
    show_badges()
elif page == "Companion":
    show_pet()
elif page == "Profile":
    show_profile()
elif page == "Settings":
    from components.navbar import show_navbar
    show_navbar()
    st.title("Settings")
    st.write("Settings coming soon.")
