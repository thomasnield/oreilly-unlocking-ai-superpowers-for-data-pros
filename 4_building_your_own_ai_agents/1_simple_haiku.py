from openai import OpenAI
from MyKey import MY_OPENAI_KEY # Replace with your actual OpenAI API key in MyKey.py

client = OpenAI(
  api_key=MY_OPENAI_KEY
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message.content)
