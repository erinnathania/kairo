import streamlit as st
import data_manager as dm
from components.navbar import show_navbar


def show_profile():
    show_navbar()

    st.title("Your Profile")
    st.caption("Help Kairo get to know you so it can personalize your experience.")
    st.divider()

    profile = dm.load_profile()

    with st.form("profile_form"):
        name_input = st.text_input("What's your name?", value=profile.get("name", ""))

        hobbies = st.multiselect(
            "What are your hobbies?",
            ["Reading", "Exercise", "Gaming", "Cooking", "Music", "Art", "Travel", "Sports", "Meditation"],
            default=profile.get("hobbies", [])
        )
        hobbies_other = st.text_input("Other hobbies (optional)", value=profile.get("hobbies_other", ""))

        routine = st.multiselect(
            "What does your daily routine look like?",
            ["Early riser", "Night owl", "Work from home", "Student", "Regular gym-goer", "Meal prepper"],
            default=profile.get("routine", [])
        )
        routine_other = st.text_input("Other routine details (optional)", value=profile.get("routine_other", ""))

        goals = st.multiselect(
            "What are your current goals?",
            ["Better sleep", "Exercise more", "Reduce stress", "Be more productive", "Learn new skills", "Eat healthier"],
            default=profile.get("goals", [])
        )
        goals_other = st.text_input("Other goals (optional)", value=profile.get("goals_other", ""))

        personality_options = ["Select...", "Introvert", "Extrovert", "Ambivert"]
        saved_personality = profile.get("personality", "Select...")
        personality_index = personality_options.index(saved_personality) if saved_personality in personality_options else 0
        personality = st.selectbox("How would you describe yourself?", personality_options, index=personality_index)

        submitted = st.form_submit_button("Save Profile")

        if submitted:
            if name_input.strip():
                dm.save_profile({
                    "name": name_input,
                    "hobbies": hobbies,
                    "hobbies_other": hobbies_other,
                    "routine": routine,
                    "routine_other": routine_other,
                    "goals": goals,
                    "goals_other": goals_other,
                    "personality": personality
                })
                st.success(f"Profile saved for {name_input}!")
            else:
                st.warning("Please enter your name to save your profile.")
