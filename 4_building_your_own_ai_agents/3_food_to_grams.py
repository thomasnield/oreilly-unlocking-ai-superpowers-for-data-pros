import openai
from MyKey import MY_OPENAI_KEY # Replace with your actual OpenAI API key in MyKey.py

class FoodMeasureAgent:
    def __init__(self):

        # Initialize OpenAI client with API key
        self.client = openai.OpenAI(api_key=MY_OPENAI_KEY)
        self.conversation_history = [
            {"role": "system",
             "content": "Convert each food measurement the user provides into grams. Only present the measurement. For example, If asked for a tablespoon of olive oil, only output '14 grams'"
             }
        ]

    def get_response(self, user_input):
        # Add user message to conversation history
        self.conversation_history.append({"role": "user", "content": user_input})

        # Get response from OpenAI
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",  # You can change to "gpt-4" if you have access
            messages=self.conversation_history,
            max_tokens=1000,
            temperature=0.7
        )

        # Extract the assistant's response
        assistant_response = response.choices[0].message.content.strip()

        # Add assistant's response to conversation history
        self.conversation_history.append({"role": "assistant", "content": assistant_response})

        return assistant_response

# Replace with your actual OpenAI API key
agent = FoodMeasureAgent()
print("Welcome! Type a food measurement and I will convert it into grams. Type 'quit' to exit.")
while True:
    user_input = input("\nYou: ")
    if user_input.lower() == 'quit':
        print("Goodbye!")
        break
    response = agent.get_response(user_input)
    print(f"AI: {response}")