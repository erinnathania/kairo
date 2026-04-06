import streamlit as st


def show_navbar():
    current = st.session_state.get("page", "Home")
    pages = ["Home", "Mind", "Journal", "Habits", "Badges", "Daily Summary"]

    col_logo, col_nav, col_profile = st.columns([1, 7, 1])

    with col_logo:
        st.markdown("### Kairo")

    with col_nav:
        default_index = pages.index(current) if current in pages else 0
        selected = st.radio(
            "nav",
            pages,
            index=default_index,
            horizontal=True,
            label_visibility="collapsed"
        )
        if selected != current:
            st.session_state.page = selected
            st.rerun()

    with col_profile:
        if st.button("Profile", use_container_width=True):
            st.session_state.page = "Profile"
            st.rerun()

    st.divider()
