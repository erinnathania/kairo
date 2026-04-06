import data_manager as dm
from datetime import datetime


def get_all_badges():
    """Check all badge conditions and return earned + locked badges."""
    moods = dm.load_mood_history()
    journal = dm.load_journal_entries()
    habits = dm.load_habits()
    habit_logs = dm.load_all_habit_logs()

    earned = []
    locked = []

    # ── CONSISTENCY BADGES (habit streaks) ────────────────
    max_streak = 0
    for habit in habits:
        streak = dm.get_habit_streak(habit["name"])
        if streak > max_streak:
            max_streak = streak

    total_habits_completed = sum(
        1 for day_logs in habit_logs.values()
        for done in day_logs.values() if done
    )

    consistency = [
        ("First Step", "Complete your first habit", total_habits_completed >= 1),
        ("Steady Flow", "Reach a 3-day streak", max_streak >= 3),
        ("Unbroken", "Reach a 7-day streak", max_streak >= 7),
        ("Momentum", "Reach a 14-day streak", max_streak >= 14),
        ("Relentless", "Reach a 30-day streak", max_streak >= 30),
    ]

    for name, desc, unlocked in consistency:
        if unlocked:
            earned.append({"name": name, "description": desc, "category": "Consistency"})
        else:
            locked.append({"name": name, "description": desc, "category": "Consistency"})

    # ── MINDFULNESS BADGES (mood check-ins) ───────────────
    total_checkins = len(moods)

    mindfulness = [
        ("Pause", "Complete your first mindfulness check-in", total_checkins >= 1),
        ("Grounded", "Complete 5 check-ins", total_checkins >= 5),
        ("Present", "Complete 20 check-ins", total_checkins >= 20),
        ("Still Mind", "Complete 50 check-ins", total_checkins >= 50),
    ]

    for name, desc, unlocked in mindfulness:
        if unlocked:
            earned.append({"name": name, "description": desc, "category": "Mindfulness"})
        else:
            locked.append({"name": name, "description": desc, "category": "Mindfulness"})

    # ── JOURNALING BADGES ─────────────────────────────────
    total_entries = len(journal)

    journaling = [
        ("First Words", "Write your first journal entry", total_entries >= 1),
        ("Honest Reflection", "Write 7 journal entries", total_entries >= 7),
        ("Deep Thinker", "Write 30 journal entries", total_entries >= 30),
        ("Inner Clarity", "Write 100 journal entries", total_entries >= 100),
    ]

    for name, desc, unlocked in journaling:
        if unlocked:
            earned.append({"name": name, "description": desc, "category": "Journaling"})
        else:
            locked.append({"name": name, "description": desc, "category": "Journaling"})

    # ── GROWTH BADGES ─────────────────────────────────────
    # Self-Aware: has enough data for pattern detection (3+ mood entries)
    has_patterns = total_checkins >= 3 and len(habit_logs) >= 3

    # Resilient: returned after 2+ days of no activity
    resilient = False
    if len(moods) >= 2:
        dates = sorted(set(m["date"] for m in moods))
        for i in range(1, len(dates)):
            from datetime import date as dt_date
            d1 = dt_date.fromisoformat(dates[i - 1])
            d2 = dt_date.fromisoformat(dates[i])
            if (d2 - d1).days >= 3:
                resilient = True
                break

    # Explorer: has 5+ different habits created
    explorer = len(habits) >= 5

    growth = [
        ("Self-Aware", "Generate your first pattern insight (3+ days of data)", has_patterns),
        ("Resilient", "Return after 2+ days of inactivity", resilient),
        ("Explorer", "Create 5 or more different habits", explorer),
    ]

    for name, desc, unlocked in growth:
        if unlocked:
            earned.append({"name": name, "description": desc, "category": "Growth"})
        else:
            locked.append({"name": name, "description": desc, "category": "Growth"})

    # ── SPECIAL HIDDEN BADGES ─────────────────────────────
    # Night Owl: 3+ check-ins after 10 PM
    night_checkins = sum(1 for m in moods if int(m["time"].split(":")[0]) >= 22)

    # Early Rise: 3+ check-ins before 7 AM
    early_checkins = sum(1 for m in moods if int(m["time"].split(":")[0]) < 7)

    # Comeback: returned after 7+ days gap
    comeback = False
    if len(moods) >= 2:
        dates = sorted(set(m["date"] for m in moods))
        for i in range(1, len(dates)):
            from datetime import date as dt_date
            d1 = dt_date.fromisoformat(dates[i - 1])
            d2 = dt_date.fromisoformat(dates[i])
            if (d2 - d1).days >= 7:
                comeback = True
                break

    special = [
        ("Night Owl", "Check in 3 times after 10 PM", night_checkins >= 3),
        ("Early Rise", "Check in 3 times before 7 AM", early_checkins >= 3),
        ("Comeback", "Return after a week away", comeback),
    ]

    for name, desc, unlocked in special:
        if unlocked:
            earned.append({"name": name, "description": desc, "category": "Special"})
        else:
            locked.append({"name": name, "description": desc, "category": "Special"})

    return earned, locked
