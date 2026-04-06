import streamlit as st
import pandas as pd
import data_manager as dm
from components.navbar import show_navbar


def show_summary():
    show_navbar()

    st.title("Daily Summary")
    st.write("Here is a look at how your day went.")
    st.divider()

    profile = dm.load_profile()
    name = profile.get("name", "there")

    st.subheader(f"A recap of your day, {name}.")

    todays_mood = dm.get_todays_mood()
    todays_journal = dm.get_todays_journal()
    todays_habits = dm.get_todays_habit_logs()
    habits = dm.load_habits()
    completed = sum(1 for h in habits if todays_habits.get(h["name"], False))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Mood Today", todays_mood["mood_label"] if todays_mood else "Not logged")
    with col2:
        st.metric("Journal Entries", len(todays_journal))
    with col3:
        st.metric("Habits Completed", f"{completed}/{len(habits)}")

    if habits:
        st.divider()
        st.subheader("Habits Breakdown")
        for habit in habits:
            done = todays_habits.get(habit["name"], False)
            streak = dm.get_habit_streak(habit["name"])
            status = "Done" if done else "Not done"
            st.markdown(f"**{habit['name']}** — {status} — {streak} day streak")

    if todays_journal:
        st.divider()
        st.subheader("Journal Highlights")
        for entry in todays_journal:
            preview = entry["entry"][:200] + ("..." if len(entry["entry"]) > 200 else "")
            st.markdown(f"> *{preview}*")

    st.divider()
    st.subheader("Patterns and Insights")

    mood_history = dm.load_mood_history()
    habit_logs = dm.load_all_habit_logs()
    journal_entries = dm.load_journal_entries()

    if len(mood_history) < 3:
        st.info("Keep using Kairo for a few more days to unlock personalized insights.")
    else:
        stress_moods = {"Anxious", "Stressed", "Sad", "Tired"}
        stressed_rates = []
        calm_rates = []

        for mood_entry in mood_history:
            day = mood_entry["date"]
            day_habits = habit_logs.get(day, {})
            if day_habits:
                rate = sum(1 for v in day_habits.values() if v) / len(day_habits)
                if mood_entry["mood_label"] in stress_moods:
                    stressed_rates.append(rate)
                else:
                    calm_rates.append(rate)

        if stressed_rates and calm_rates:
            avg_stressed = sum(stressed_rates) / len(stressed_rates)
            avg_calm = sum(calm_rates) / len(calm_rates)

            if avg_calm > avg_stressed + 0.1:
                st.warning(
                    f"You complete {int(avg_calm * 100)}% of habits on good days "
                    f"vs {int(avg_stressed * 100)}% on stressful days. "
                    f"Try setting smaller habits on tough days."
                )
            else:
                st.success("You stay consistent with your habits regardless of your mood. That is a real strength.")

        if journal_entries:
            mood_counts = {}
            for e in journal_entries:
                m = e.get("mood", "Unknown")
                mood_counts[m] = mood_counts.get(m, 0) + 1
            most_common = max(mood_counts, key=mood_counts.get)
            st.info(f"You journal most when feeling {most_common}.")

        if len(mood_history) >= 5:
            day_scores = {}
            for entry in mood_history:
                try:
                    day_name = pd.to_datetime(entry["date"]).strftime("%A")
                    day_scores.setdefault(day_name, []).append(entry["mood_score"])
                except Exception:
                    continue
            if day_scores:
                avg_by_day = {d: sum(scores) / len(scores) for d, scores in day_scores.items()}
                best_day = max(avg_by_day, key=avg_by_day.get)
                st.info(f"Your best mood day tends to be {best_day}.")

    if len(mood_history) >= 2:
        st.divider()
        st.subheader("Mood Over Time")
        df = pd.DataFrame(mood_history)
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")
        st.line_chart(df.set_index("date")["mood_score"])

    st.divider()
    if habits and completed == len(habits):
        st.success(f"Perfect day, {name}. You hit all your habits.")
    elif completed > 0:
        st.info(f"Good effort today, {name}. Every day you show up is progress.")
    else:
        st.info(f"Tomorrow is a fresh start, {name}.")
