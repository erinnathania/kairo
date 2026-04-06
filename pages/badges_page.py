import streamlit as st
from components.navbar import show_navbar
from badges import get_all_badges


def show_badges():
    show_navbar()

    st.title("Badges")
    st.write("Earn badges by being consistent, reflective, and showing up for yourself.")
    st.divider()

    earned, locked = get_all_badges()

    # Summary
    total = len(earned) + len(locked)
    st.subheader(f"{len(earned)} of {total} badges earned")
    st.progress(len(earned) / total if total > 0 else 0)
    st.write("")

    # ── Earned badges ─────────────────────────────────────
    if earned:
        st.subheader("Earned")
        categories = {}
        for badge in earned:
            categories.setdefault(badge["category"], []).append(badge)

        for category, badges in categories.items():
            st.markdown(f"**{category}**")
            cols = st.columns(min(len(badges), 4))
            for i, badge in enumerate(badges):
                with cols[i % 4]:
                    with st.container(border=True):
                        st.markdown(f"**{badge['name']}**")
                        st.caption(badge["description"])
            st.write("")

    # ── Locked badges ─────────────────────────────────────
    if locked:
        st.subheader("Locked")
        categories = {}
        for badge in locked:
            categories.setdefault(badge["category"], []).append(badge)

        for category, badges in categories.items():
            st.markdown(f"**{category}**")
            cols = st.columns(min(len(badges), 4))
            for i, badge in enumerate(badges):
                with cols[i % 4]:
                    with st.container(border=True):
                        st.markdown(f"~~{badge['name']}~~")
                        st.caption(badge["description"])
            st.write("")
