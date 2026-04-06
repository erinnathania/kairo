import streamlit as st
import time
import data_manager as dm
from components.navbar import show_navbar

# Rule-based recommendations per mood
# TODO: Replace with AI API calls in a later session
MOOD_DATA = {
    "Anxious": {
        "exercises": [
            "Box Breathing: Inhale 4s, Hold 4s, Exhale 4s, Hold 4s",
            "5-4-3-2-1 Grounding: Name 5 things you see, 4 you hear, 3 you can touch, 2 you smell, 1 you taste",
            "Progressive Muscle Relaxation: Tense and release each muscle group from feet to face"
        ],
        "task_tip": "Break your tasks into very small steps. Focus on just the next 10 minutes.",
        "affirmation": "You are capable of handling what comes your way. One breath at a time."
    },
    "Stressed": {
        "exercises": [
            "4-7-8 Breathing: Inhale 4s, Hold 7s, Exhale 8s",
            "Take a 5-minute walk outside or around your space",
            "Write down your 3 biggest stressors and one small action for each"
        ],
        "task_tip": "On stressful days, tackle your hardest task first when your energy is freshest.",
        "affirmation": "Stress is temporary. You have gotten through tough days before."
    },
    "Sad": {
        "exercises": [
            "Gentle movement: 5 minutes of slow stretching",
            "Reach out — send a message to someone you trust",
            "Do one small thing that usually brings you comfort"
        ],
        "task_tip": "Be gentle with yourself today. Even completing one small task is a real win.",
        "affirmation": "It is okay not to be okay. Every feeling passes. You are not alone."
    },
    "Tired": {
        "exercises": [
            "Take a 10-20 minute nap if possible",
            "Splash cold water on your face and wrists",
            "Energizing breath: 30 seconds of quick inhales and exhales through your nose"
        ],
        "task_tip": "Work in short 25-minute bursts with 5-minute breaks (Pomodoro technique).",
        "affirmation": "Rest is productive. Your body is telling you something real."
    },
    "Calm": {
        "exercises": [
            "Take a moment to appreciate this feeling — it is worth noticing",
            "Use this calm energy for creative or deep focused work",
            "Mindful observation: spend 2 minutes noticing your surroundings without judgment"
        ],
        "task_tip": "This is a great time for deep work or tackling complex problems.",
        "affirmation": "You are grounded and present. This is your natural state."
    },
    "Happy": {
        "exercises": [
            "Share your good mood — send a kind message to someone",
            "Use this energy to tackle something you have been putting off",
            "Write down what is making you feel good to revisit on harder days"
        ],
        "task_tip": "Great day to push toward a big goal — your energy and optimism are high.",
        "affirmation": "Soak in this feeling. You deserve good days like this."
    },
    "Motivated": {
        "exercises": [
            "Channel this energy — write your top 3 priorities for today",
            "Start the task you have been procrastinating on",
            "Set a clear intention: what do you want to accomplish today?"
        ],
        "task_tip": "Strike while the iron is hot — start your most important task right now.",
        "affirmation": "This energy is yours. Use it wisely and enjoy the momentum."
    }
}


def show_mindfulness():
    show_navbar()

    st.title("Mind")
    st.write("Check in with yourself. How are you really feeling right now?")
    st.divider()

    st.subheader("Daily Check-In")
    mood_options = list(MOOD_DATA.keys())
    selected_mood = st.selectbox("How are you feeling?", ["Select your mood..."] + mood_options)
    mood_score = st.slider("Rate your overall mood (1 = very low, 10 = great)", 1, 10, 5)
    notes = st.text_input("Any specific thoughts right now? (optional)")

    if st.button("Check In"):
        if selected_mood == "Select your mood...":
            st.warning("Please select a mood first.")
        else:
            dm.save_mood_entry(mood_score, selected_mood, notes)
            st.success(f"Checked in. You are feeling {selected_mood} today (score: {mood_score}/10)")
            st.divider()

            data = MOOD_DATA[selected_mood]

            st.subheader(f"Recommendations for when you feel {selected_mood}")
            st.markdown("**Try one of these:**")
            for exercise in data["exercises"]:
                st.markdown(f"- {exercise}")

            st.divider()
            st.info(f"Task Tip: {data['task_tip']}")
            st.success(data["affirmation"])

    st.divider()
    st.subheader("Box Breathing Exercise")
    st.caption("A simple technique to calm your nervous system. Inhale, Hold, Exhale, Hold — 4 seconds each.")

    if st.button("Start Breathing Exercise (3 rounds)"):
        placeholder = st.empty()
        steps = [
            ("Inhale...", 4),
            ("Hold...", 4),
            ("Exhale...", 4),
            ("Hold...", 4),
        ]
        for round_num in range(1, 4):
            for step_text, duration in steps:
                for i in range(duration, 0, -1):
                    placeholder.markdown(f"### Round {round_num}/3 — {step_text} {i}s")
                    time.sleep(1)
        placeholder.markdown("### Well done. Notice how you feel now.")

    st.divider()
    st.subheader("Recent Check-Ins")
    history = dm.load_mood_history()

    if not history:
        st.caption("No check-ins yet. Start above.")
    else:
        for entry in reversed(history[-5:]):
            note = f" — {entry['notes']}" if entry.get("notes") else ""
            st.markdown(f"**{entry['date']}** at {entry['time']} — {entry['mood_label']} ({entry['mood_score']}/10){note}")
