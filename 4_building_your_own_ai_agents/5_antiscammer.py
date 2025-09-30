import openai
from MyKey import MY_OPENAI_KEY # Replace with your actual OpenAI API key in MyKey.py

# Initialize OpenAI client
client = openai.OpenAI(api_key=MY_OPENAI_KEY)

# --- Agent 1: Scam Detector ---
class ScamDetector:
    def __init__(self, client):
        self.client = client

    def analyze_email(self, email_text):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Your job is to classify scam emails based on the text contents user will provide. Only reply with 'YES' or 'NO' where 'YES' is a scam."},
                {"role": "user", "content": email_text}
            ],
            max_tokens=10,
            temperature=0.1
        )
        return response.choices[0].message.content.strip()

# --- Agent 2: Time Waster ---
class TimeWaster():
    def __init__(self, client, signature_name="Thomas"):
        self.client = client
        self.signature_name = signature_name

    def craft_response(self, email_text):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Write a long response to this scam email that is likely to keep the scammer engaged. Do not volunteer any personal information. Just waste the scammer's time so they stay too busy to target real victims. Sign off as " + self.signature_name},
                {"role": "user", "content": email_text}
            ],
            max_tokens=500,
            temperature=0.95 # increase temperature to make response more crazy
        )
        return response.choices[0].message.content.strip()

# --- Multi-Agent System ---
class EmailHandler:
    def __init__(self, client):
        self.scam_detector = ScamDetector(client)
        self.time_waster = TimeWaster(client)

    def process_email(self, email_text):
        # Step 1: Detect scam
        status = self.scam_detector.analyze_email(email_text)
        print(f"Email: {email_text}")
        print(f"Scam Detector: {status}")

        # Step 2: If scam, waste time
        if status == "YES":
            reply = self.time_waster.craft_response(email_text)
            print(f"Time-Wasting Reply: {reply}")
        else:
            print("No reply generated.")
        print("---")

# Run the system
handler = EmailHandler(client)


# Simulated email examples
emails = [
    "Dear sir, you’ve won $1M! Send your bank details to claim it now! Sincerely, The Grand Prize Association",
    "Hi team, meeting at 3 PM today, please prepare your updates.",
    "Urgent: Your account is hacked, send password to fix it. -The Amazon Security Team",
    "Dude, where are you? The meeting is starting right now. Everything alright?",
    "Dear sir, my father (a noble prince of Nigeria) was killed by assassins. Please help me wire his fortune and i will pay you handsomely. Sincerely, Matthew"
]

for email in emails:
    handler.process_email(email)
    input("Press enter to continue next email.")