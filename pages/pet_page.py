import streamlit as st
import data_manager as dm
from components.navbar import show_navbar

# Pet definitions — visuals are placeholders, swap with images later
PETS = {
    "Lumis": {
        "description": "A light-based creature. Calm and radiant. Grows brighter as you grow.",
        "personality": "Gentle, warm, encouraging",
    },
    "Aven": {
        "description": "A bird-like intelligence symbol. Sharp and curious. Learns alongside you.",
        "personality": "Curious, energetic, playful",
    },
    "Rye": {
        "description": "A time spirit form. Patient and wise. Helps you value your journey.",
        "personality": "Wise, steady, reflective",
    },
    "Nox": {
        "description": "A calm, night-based entity. Quiet and grounding. Thrives in stillness.",
        "personality": "Quiet, protective, soothing",
    },
}


def get_pet_status(stats):
    """Describe how the pet is doing based on stats."""
    avg = (stats["energy"] + stats["mood"] + stats["growth"]) / 3
    if avg >= 80:
        return "Thriving", "Your companion is happy and full of energy."
    elif avg >= 50:
        return "Content", "Your companion is doing well. Keep it up."
    elif avg >= 25:
        return "Needs attention", "Your companion could use some care. Try checking in or completing a habit."
    else:
        return "Resting", "Your companion is waiting for you. Any small action helps."


def get_interaction_summary():
    """Show what actions feed the pet."""
    today = dm.date.today().isoformat()
    moods = dm.load_mood_history()
    journal = dm.load_journal_entries()
    habit_logs = dm.get_todays_habit_logs()

    resting = sum(1 for m in moods if m["date"] == today)
    feeding = sum(1 for j in journal if j["date"] == today)
    playing = sum(1 for v in habit_logs.values() if v)

    return resting, feeding, playing


def show_pet():
    show_navbar()

    st.title("Your Companion")
    st.write("Your companion grows and evolves based on your daily activity.")
    st.divider()

    pet_data = dm.load_pet()

    # ── Pet selection (if no pet chosen yet) ──────────────
    if not pet_data.get("name"):
        st.subheader("Choose your companion")
        st.write("Pick a companion that resonates with you. This is who will grow alongside you.")
        st.write("")

        cols = st.columns(4)
        for i, (pet_name, info) in enumerate(PETS.items()):
            with cols[i]:
                with st.container(border=True):
                    st.markdown(f"### {pet_name}")
                    st.write(info["description"])
                    st.caption(f"Personality: {info['personality']}")
                    if st.button(f"Choose {pet_name}", key=f"pick_{pet_name}", use_container_width=True):
                        dm.save_pet({"name": pet_name, "chosen": dm.date.today().isoformat()})
                        st.rerun()
        return

    # ── Pet display ───────────────────────────────────────
    chosen_name = pet_data["name"]
    pet_info = PETS.get(chosen_name, {})
    stats = dm.get_pet_stats()
    status_label, status_desc = get_pet_status(stats)

    col_pet, col_stats = st.columns([2, 3])

    with col_pet:
        with st.container(border=True):
            st.subheader(chosen_name)
            st.caption(pet_info.get("personality", ""))
            st.write("")
            # Placeholder for pet visual — replace with image later
            st.markdown(f"*[ {chosen_name} illustration goes here ]*")
            st.write("")
            st.markdown(f"**Status:** {status_label}")
            st.caption(status_desc)

    with col_stats:
        st.subheader("Stats")
        st.write("")

        st.markdown("**Energy** — Based on your daily activity")
        st.progress(stats["energy"] / 100)
        st.caption(f"{stats['energy']}%")
        st.write("")

        st.markdown("**Mood** — Based on your emotional consistency")
        st.progress(stats["mood"] / 100)
        st.caption(f"{stats['mood']}%")
        st.write("")

        st.markdown("**Growth** — Based on your habit completion this week")
        st.progress(stats["growth"] / 100)
        st.caption(f"{stats['growth']}%")

    # ── Interactions today ────────────────────────────────
    st.divider()
    st.subheader("Today's Interactions")
    resting, feeding, playing = get_interaction_summary()

    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.markdown("**Resting**")
            st.caption("Mindfulness check-ins")
            st.metric("Sessions today", resting)
    with col2:
        with st.container(border=True):
            st.markdown("**Feeding**")
            st.caption("Journal entries written")
            st.metric("Entries today", feeding)
    with col3:
        with st.container(border=True):
            st.markdown("**Playing**")
            st.caption("Habits completed")
            st.metric("Completed today", playing)

    # ── Tips ──────────────────────────────────────────────
    st.divider()
    if stats["energy"] < 30:
        st.info("Tip: Complete a habit or check in with your mood to boost your companion's energy.")
    if stats["mood"] < 30:
        st.info("Tip: Regular mindfulness check-ins help stabilize your companion's mood.")
    if stats["growth"] < 30:
        st.info("Tip: Consistent habit completion helps your companion grow over time.")

    # ── Change pet option ─────────────────────────────────
    st.divider()
    with st.expander("Change companion"):
        st.caption("You can switch to a different companion at any time.")
        new_pet = st.selectbox(
            "Switch to",
            ["Select..."] + [p for p in PETS.keys() if p != chosen_name]
        )
        if st.button("Switch") and new_pet != "Select...":
            dm.save_pet({"name": new_pet, "chosen": dm.date.today().isoformat()})
            st.rerun()
