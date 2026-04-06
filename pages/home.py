import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import data_manager as dm
from components.navbar import show_navbar


def navigate_to(page):
    st.session_state.page = page
    st.rerun()


def feature_card(title, description, button_key, page_name):
    with st.container(border=True):
        st.markdown(f"### {title}")
        st.write(description)
        st.write("")
        if st.button(f"Open {title} →", key=button_key, use_container_width=True):
            navigate_to(page_name)


def show_home():
    show_navbar()

    profile = dm.load_profile()
    name = profile.get("name", "")

    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good morning"
    elif hour < 17:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    st.title(f"{greeting}{', ' + name if name else ''}.")
    st.caption("Here is your overview for today.")
    st.divider()

    # ── Quick stats ───────────────────────────────────────
    todays_mood = dm.get_todays_mood()
    todays_journal = dm.get_todays_journal()
    todays_habits = dm.get_todays_habit_logs()
    habits = dm.load_habits()
    completed_today = sum(1 for h in habits if todays_habits.get(h["name"], False))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Mood Today", todays_mood["mood_label"] if todays_mood else "Not checked in")
    with col2:
        st.metric("Journal Entries", len(todays_journal))
    with col3:
        st.metric("Habits Completed", f"{completed_today}/{len(habits)}")

    st.divider()

    # ── Feature cards ─────────────────────────────────────
    st.subheader("What would you like to do?")
    st.write("")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        feature_card(
            "Mind",
            "Check in with your mood and get grounding exercises tailored to how you feel.",
            "card_mind", "Mind"
        )
    with col2:
        feature_card(
            "Journal",
            "Reflect on your day with prompts based on your mood and past entries.",
            "card_journal", "Journal"
        )
    with col3:
        feature_card(
            "Habits",
            "Track your daily habits, build streaks, and earn badges for consistency.",
            "card_habits", "Habits"
        )
    with col4:
        feature_card(
            "Daily Summary",
            "See your accomplishments, patterns, and personalized insights from today.",
            "card_summary", "Daily Summary"
        )

    st.divider()

    # ── Weekly tracker ────────────────────────────────────
    st.subheader("Your Week at a Glance")

    today = date.today()
    week_dates = [(today - timedelta(days=i)).isoformat() for i in range(6, -1, -1)]
    week_labels = [(today - timedelta(days=i)).strftime("%a %d") for i in range(6, -1, -1)]

    mood_history = dm.load_mood_history()
    habit_logs = dm.load_all_habit_logs()

    mood_by_date = {entry["date"]: entry["mood_score"] for entry in mood_history}
    mood_scores = [mood_by_date.get(d) for d in week_dates]

    habit_rates = []
    for d in week_dates:
        day_logs = habit_logs.get(d, {})
        if day_logs and habits:
            rate = sum(1 for v in day_logs.values() if v) / len(habits) * 100
        else:
            rate = None
        habit_rates.append(rate)

    tab1, tab2 = st.tabs(["Mood This Week", "Habit Completion This Week"])

    with tab1:
        if any(v is not None for v in mood_scores):
            df_mood = pd.DataFrame({
                "Day": week_labels,
                "Mood Score": mood_scores
            }).set_index("Day")
            st.line_chart(df_mood)
        else:
            st.caption("No mood data yet. Check in on the Mind page to start tracking.")

    with tab2:
        if any(v is not None for v in habit_rates):
            df_habits = pd.DataFrame({
                "Day": week_labels,
                "Completion %": habit_rates
            }).set_index("Day")
            st.bar_chart(df_habits)
        else:
            st.caption("No habit data yet. Log your habits to start tracking your week.")
