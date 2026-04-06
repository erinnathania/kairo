import streamlit as st
import data_manager as dm
from datetime import date
from components.navbar import show_navbar


def get_badge(streak):
    if streak >= 30:
        return "Legend (30+ days)"
    elif streak >= 14:
        return "Diamond (14+ days)"
    elif streak >= 7:
        return "Gold (7+ days)"
    elif streak >= 3:
        return "Silver (3+ days)"
    elif streak >= 1:
        return "Bronze (1+ day)"
    else:
        return "Just starting"


def show_habits():
    show_navbar()

    st.title("Habits")
    st.write("Build habits that actually stick. Small steps, big change.")
    st.divider()

    st.subheader("Add a New Habit")
    with st.form("add_habit_form"):
        col1, col2 = st.columns(2)
        with col1:
            new_habit = st.text_input("Habit name", placeholder="e.g. Drink 8 glasses of water")
        with col2:
            category = st.selectbox("Category", ["Health", "Mindfulness", "Productivity", "Learning", "Social", "Other"])

        submitted = st.form_submit_button("Add Habit")
        if submitted:
            if new_habit.strip():
                habits = dm.load_habits()
                if not any(h["name"] == new_habit.strip() for h in habits):
                    habits.append({
                        "name": new_habit.strip(),
                        "category": category,
                        "created": date.today().isoformat()
                    })
                    dm.save_habits(habits)
                    st.success(f"Habit '{new_habit.strip()}' added.")
                    st.rerun()
                else:
                    st.warning("That habit already exists.")
            else:
                st.warning("Please enter a habit name.")

    st.divider()
    st.subheader("Today's Habits")
    habits = dm.load_habits()
    todays_logs = dm.get_todays_habit_logs()

    if not habits:
        st.info("No habits yet. Add your first habit above.")
    else:
        for habit in habits:
            streak = dm.get_habit_streak(habit["name"])
            is_done = todays_logs.get(habit["name"], False)

            col1, col2, col3 = st.columns([3, 1, 2])
            with col1:
                checked = st.checkbox(
                    f"**{habit['name']}** — {habit['category']}",
                    value=is_done,
                    key=f"habit_{habit['name']}"
                )
                if checked != is_done:
                    dm.log_habit_completion(habit["name"], checked)
                    if checked:
                        st.balloons()
                    st.rerun()
            with col2:
                st.caption(f"{streak} day streak")
            with col3:
                st.caption(get_badge(streak))

        completed = sum(1 for h in habits if todays_logs.get(h["name"], False))
        total = len(habits)
        st.divider()
        st.progress(completed / total if total > 0 else 0)
        st.caption(f"{completed} of {total} habits completed today")

        if total > 0 and completed == total:
            st.success("You completed all your habits today.")
        elif completed > 0:
            st.info(f"{total - completed} more to go.")

    if habits:
        st.divider()
        st.subheader("Manage Habits")
        habit_to_delete = st.selectbox(
            "Remove a habit",
            ["Select..."] + [h["name"] for h in habits]
        )
        if st.button("Remove Habit") and habit_to_delete != "Select...":
            habits = [h for h in habits if h["name"] != habit_to_delete]
            dm.save_habits(habits)
            st.success(f"Removed '{habit_to_delete}'")
            st.rerun()
