import streamlit as st


def show_navbar():
    pages = ["Mind", "Journal", "Habits", "Daily Summary"]
    current = st.session_state.get("page", "Home")

    st.markdown("""
    <style>
    .navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 0px;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 24px;
    }
    .navbar-brand {
        font-size: 20px;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    </style>
    <div class="navbar">
        <span class="navbar-brand">Kairo</span>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns([1, 1, 1, 1, 1, 3, 1])
    nav_items = ["Home", "Mind", "Journal", "Habits", "Daily Summary"]

    for i, (col, nav_page) in enumerate(zip(cols[:5], nav_items)):
        with col:
            label = f"**{nav_page}**" if current == nav_page else nav_page
            if st.button(label, key=f"nav_{nav_page}", use_container_width=True):
                st.session_state.page = nav_page
                st.rerun()

    with cols[6]:
        if st.button("Profile", key="nav_profile", use_container_width=True):
            st.session_state.page = "Profile"
            st.rerun()

    st.divider()
