import json
from pathlib import Path

import requests

# =====================================================
# CONFIG
# =====================================================

import os

BOT_TOKEN = os.environ["BOT_TOKEN"]

CHANNELS = [
    "@upsclog",
    "@upsc_daily_pyq"
]

QUESTIONS_FILE = "questions.txt"

POLLS_PER_RUN = 5

# =====================================================


INTRO = """📚🔥 <b>Daily NCERT & GS MCQ Quiz</b> 🔥📚

🎯 Welcome to today's practice session!

Boost your preparation with carefully selected MCQs covering <b>NCERTs, Geography, History, Polity, Economy, Environment, Science & Current Affairs.</b>

🏆 Perfect for aspirants preparing for <b>UPSC CSE, SSC, CDS, CAPF, State PSCs, Railways, Banking</b> and other competitive examinations.

🚀 Best of Luck!!
👇 Let's Begin 👇
"""


OUTRO = """📖━━━━━━━━📖

🌟 <b>Remember...</b>

These questions are carefully sourced from <b>NCERTs</b> and cover the fundamental concepts that form the <b>bedrock of UPSC Prelims</b> and many other competitive examinations.

📚 Revise regularly.
🧠 Learn from your mistakes.
🚀 Stay consistent.

<b>Success isn't about studying more—it's about revising better.</b>

💙 See you in the next quiz!

"""

def send_message(channel, text):
    """Send introductory message."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": channel,
        "text": text,
        "parse_mode": "HTML"
    }

    r = requests.post(url, data=payload)

    if r.ok:
        print(f"[{channel}] Intro message sent.")
        return True
    else:
        print(f"[{channel}] Intro failed.")
        print(r.text)
        return False


def send_poll(channel, question):
    """Send one quiz poll."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPoll"

    payload = {
        "chat_id": channel,
        "question": question["question"],
        "options": json.dumps(question["options"]),
        "type": "quiz",
        "correct_option_id": question["answer"],
        "is_anonymous": True
    }

    r = requests.post(url, data=payload)

    if r.ok:
        print(f"[{channel}] Posted: {question['question']}")
        return True
    else:
        print(f"[{channel}] Failed:")
        print(r.text)
        return False


def load_questions():
    file = Path(QUESTIONS_FILE)

    if not file.exists():
        raise FileNotFoundError(f"{QUESTIONS_FILE} not found.")

    with file.open("r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    return lines


def rotate_questions(lines, used):
    remaining = lines[used:]
    moved = lines[:used]

    with open(QUESTIONS_FILE, "w", encoding="utf-8") as f:
        for line in remaining + moved:
            f.write(line + "\n")


def main():

    lines = load_questions()

    if len(lines) == 0:
        print("No questions found.")
        return

    count = min(POLLS_PER_RUN, len(lines))

    current_questions = lines[:count]

    # Post to every channel
    for channel in CHANNELS:

        print(f"\nPosting to {channel}")

        send_message(channel, INTRO)

        for line in current_questions:

            try:
                question = json.loads(line)
                send_poll(channel, question)

            except Exception as e:
                print("Invalid JSON:")
                print(e)
         # Send ending message
        send_message(channel, OUTRO)

    # Rotate file after successful posting loop
    rotate_questions(lines, count)

    print("\n====================================")
    print(f"Rotated {count} questions.")
    print("Done!")
    print("====================================")


if __name__ == "__main__":
    main()
