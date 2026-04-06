import json
import os
from datetime import datetime, date, timedelta

DATA_DIR = "data"


def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


# ── PROFILE ──────────────────────────────────────────────

def save_profile(profile_data):
    ensure_data_dir()
    with open(f"{DATA_DIR}/profile.json", "w") as f:
        json.dump(profile_data, f, indent=2)


def load_profile():
    try:
        with open(f"{DATA_DIR}/profile.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


# ── MOOD ─────────────────────────────────────────────────

def save_mood_entry(mood_score, mood_label, notes=""):
    ensure_data_dir()
    entries = load_mood_history()
    entries.append({
        "date": date.today().isoformat(),
        "time": datetime.now().strftime("%H:%M"),
        "mood_score": mood_score,
        "mood_label": mood_label,
        "notes": notes
    })
    with open(f"{DATA_DIR}/moods.json", "w") as f:
        json.dump(entries, f, indent=2)


def load_mood_history():
    try:
        with open(f"{DATA_DIR}/moods.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def get_todays_mood():
    today = date.today().isoformat()
    history = load_mood_history()
    todays = [e for e in history if e["date"] == today]
    return todays[-1] if todays else None


# ── JOURNAL ──────────────────────────────────────────────

def save_journal_entry(mood_label, prompt, entry_text):
    ensure_data_dir()
    entries = load_journal_entries()
    entries.append({
        "date": date.today().isoformat(),
        "time": datetime.now().strftime("%H:%M"),
        "mood": mood_label,
        "prompt": prompt,
        "entry": entry_text
    })
    with open(f"{DATA_DIR}/journal.json", "w") as f:
        json.dump(entries, f, indent=2)


def load_journal_entries():
    try:
        with open(f"{DATA_DIR}/journal.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def get_todays_journal():
    today = date.today().isoformat()
    return [e for e in load_journal_entries() if e["date"] == today]


# ── HABITS ───────────────────────────────────────────────

def save_habits(habits_list):
    ensure_data_dir()
    with open(f"{DATA_DIR}/habits.json", "w") as f:
        json.dump(habits_list, f, indent=2)


def load_habits():
    try:
        with open(f"{DATA_DIR}/habits.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def log_habit_completion(habit_name, completed):
    ensure_data_dir()
    today = date.today().isoformat()
    logs = load_all_habit_logs()
    if today not in logs:
        logs[today] = {}
    logs[today][habit_name] = completed
    with open(f"{DATA_DIR}/habit_logs.json", "w") as f:
        json.dump(logs, f, indent=2)


def load_all_habit_logs():
    try:
        with open(f"{DATA_DIR}/habit_logs.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def get_todays_habit_logs():
    today = date.today().isoformat()
    logs = load_all_habit_logs()
    return logs.get(today, {})


def get_habit_streak(habit_name):
    logs = load_all_habit_logs()
    streak = 0
    check_date = date.today()
    while True:
        date_str = check_date.isoformat()
        if date_str in logs and logs[date_str].get(habit_name, False):
            streak += 1
            check_date -= timedelta(days=1)
        else:
            break
    return streak


# ── PET ─────────────────────────────────────────────────

def save_pet(pet_data):
    ensure_data_dir()
    with open(f"{DATA_DIR}/pet.json", "w") as f:
        json.dump(pet_data, f, indent=2)


def load_pet():
    try:
        with open(f"{DATA_DIR}/pet.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def get_pet_stats():
    """Calculate pet stats from today's user activity."""
    today = date.today().isoformat()
    moods = load_mood_history()
    journal = load_journal_entries()
    habits = load_habits()
    habit_logs = get_todays_habit_logs()

    # Energy: based on total actions taken today
    todays_checkins = sum(1 for m in moods if m["date"] == today)
    todays_entries = sum(1 for j in journal if j["date"] == today)
    todays_habits_done = sum(1 for v in habit_logs.values() if v)
    total_actions = todays_checkins + todays_entries + todays_habits_done
    energy = min(total_actions * 20, 100)

    # Mood: based on mood score consistency (average of recent scores)
    recent_moods = [m["mood_score"] for m in moods[-7:]]
    if recent_moods:
        mood = int(sum(recent_moods) / len(recent_moods) * 10)
        mood = min(mood, 100)
    else:
        mood = 0

    # Growth: based on habit completion rate over the past 7 days
    all_logs = load_all_habit_logs()
    if habits:
        week_dates = [(date.today() - timedelta(days=i)).isoformat() for i in range(7)]
        completed = 0
        possible = 0
        for d in week_dates:
            day_logs = all_logs.get(d, {})
            possible += len(habits)
            completed += sum(1 for h in habits if day_logs.get(h["name"], False))
        growth = int(completed / possible * 100) if possible > 0 else 0
    else:
        growth = 0

    return {"energy": energy, "mood": mood, "growth": growth}
