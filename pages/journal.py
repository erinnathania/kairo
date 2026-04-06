import streamlit as st
import data_manager as dm
from components.navbar import show_navbar

# Rule-based journal prompts based on mood
# TODO: Replace with AI API calls in a later session
JOURNAL_PROMPTS = {
    "Anxious": [
        "What specific thing is making you anxious right now? Write it out in as much detail as you can.",
        "What is the worst case scenario you are imagining? How realistic is it really?",
        "What has helped you get through anxious moments in the past?"
    ],
    "Stressed": [
        "What are the top 3 things stressing you out right now?",
        "What is within your control today, and what is not?",
        "If a close friend was in your exact situation, what would you tell them?"
    ],
    "Sad": [
        "What are you feeling sad about? Let it all out here — no filter needed.",
        "What small thing brought even a tiny moment of comfort or warmth today?",
        "What do you need right now that you are not getting?"
    ],
    "Tired": [
        "What has been draining your energy lately?",
        "What would feel like true, deep rest for you right now?",
        "What could you say no to this week to protect your energy?"
    ],
    "Calm": [
        "What helped you reach this calm state today?",
        "What intentions do you want to set for the rest of your day?",
        "What are you genuinely grateful for in this moment?"
    ],
    "Happy": [
        "What is making you happy today? Describe it in as much detail as possible.",
        "Who or what contributed to this good mood?",
        "What recent win — big or small — are you most proud of?"
    ],
    "Motivated": [
        "What are you most excited to work on or achieve right now?",
        "What would a truly successful day look like for you today?",
        "What big goal feels possible and within reach when you are in this mindset?"
    ]
}

DEFAULT_PROMPTS = [
    "How are you feeling today, and why?",
    "What is one thing you want to focus on today?",
    "What is something you are grateful for right now?"
]


def show_journal():
    show_navbar()

    st.title("Journal")
    st.write("Reflect on your day. Your entries are private and stored only on your device.")
    st.divider()

    todays_mood = dm.get_todays_mood()

    if todays_mood:
        st.info(f"Your mood today: {todays_mood['mood_label']} — here is a prompt based on how you are feeling.")
        prompts = JOURNAL_PROMPTS.get(todays_mood["mood_label"], DEFAULT_PROMPTS)
    else:
        st.info("Head to Mind first to check in — you will get prompts personalized to your mood.")
        prompts = DEFAULT_PROMPTS

    selected_prompt = st.selectbox("Choose a prompt (or ignore it and write freely below):", prompts)
    st.markdown(f"**{selected_prompt}**")

    entry_text = st.text_area(
        "Write your entry here...",
        height=250,
        placeholder="Start writing... there are no rules. This space is just for you."
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Save Entry"):
            if entry_text.strip():
                mood_label = todays_mood["mood_label"] if todays_mood else "Not checked in"
                dm.save_journal_entry(mood_label, selected_prompt, entry_text)
                st.success("Entry saved.")
            else:
                st.warning("Write something first before saving.")

    st.divider()
    st.subheader("Past Entries")
    entries = dm.load_journal_entries()

    if not entries:
        st.caption("No entries yet. Start writing above.")
    else:
        for entry in reversed(entries[-5:]):
            with st.expander(f"{entry['date']} at {entry['time']} — Feeling: {entry['mood']}"):
                st.caption(f"Prompt: {entry['prompt']}")
                st.write(entry["entry"])
