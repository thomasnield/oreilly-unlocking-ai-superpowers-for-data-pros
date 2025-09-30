import openai
from MyKey import MY_OPENAI_KEY # Replace with your actual OpenAI API key in MyKey.py

class WorkoutBuddy:
    def __init__(self):

        # Initialize OpenAI client with API key
        self.client = openai.OpenAI(api_key=MY_OPENAI_KEY)
        self.conversation_history = [
            {"role": "system",
             "content": """"
             You are a helpful workout assistant to keep me motivated and track the user's sets. 
             The program is simple and sinister. 10 sets of kettlebell swings and then 10 turkish getups. 
             The user will let you know when each set is done. Keep count for them. 
             
             Limit to two sentences and keep it brief, but motivational.
             """
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
agent = WorkoutBuddy()
print("Welcome! Let's get to our workout! Type 'quit' to exit.")
while True:
    user_input = input("\nYou: ")
    if user_input.lower() == 'quit':
        print("Goodbye!")
        break
    response = agent.get_response(user_input)
    print(f"AI: {response}")