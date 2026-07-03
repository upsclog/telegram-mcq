import json
import random
import time
from pathlib import Path

import requests
import schedule

# =====================================================
# CONFIG
# =====================================================

os.getenv("BOT_TOKEN")

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
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": channel,
        "text": text,
        "parse_mode": "HTML"
    }

    r = requests.post(url, data=payload)

    if r.ok:
        print(f"[{channel}] Message sent.")
        return True
    else:
        print(f"[{channel}] Message failed.")
        print(r.text)
        return False


def send_poll(channel, question):
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
        return [line.strip() for line in f if line.strip()]


def main():

    lines = load_questions()

    if not lines:
        print("No questions found.")
        return

    count = min(POLLS_PER_RUN, len(lines))
    current_questions = random.sample(lines, count)

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

        send_message(channel, OUTRO)

    print("\n====================================")
    print(f"Posted {count} random questions.")
    print("Done!")
    print("====================================")


# =====================================================
# Scheduler
# =====================================================

def scheduled_job():
    print("\nStarting scheduled job...")
    try:
        main()
    except Exception as e:
        print("Error:", e)


# Change this to your preferred time (24-hour format)
schedule.every().day.at("12:35").do(scheduled_job)

print("Bot is running.")
print("Waiting for 12:35 every day...")

while True:
    schedule.run_pending()
    time.sleep(10)
