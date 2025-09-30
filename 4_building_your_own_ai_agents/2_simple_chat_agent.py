import openai
from MyKey import MY_OPENAI_KEY # Replace with your actual OpenAI API key in MyKey.py

# Set up your OpenAI API key (replace with your actual key)
openai.api_key = MY_OPENAI_KEY

class SimpleChatAgent:
    def __init__(self):
        # Store conversation history
        self.conversation_history = [
            {"role": "system", "content": "You are a helpful AI assistant."}
        ]
    
    def get_response(self, user_input):
        # Add user's message to conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        try:
            # Make API call to OpenAI
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=self.conversation_history,
                max_tokens=250,        # Limit response length
                temperature=0.7        # Controls creativity (0-1)
            )
            
            # Get AI's response
            ai_response = response.choices[0].message.content
            
            # Add AI's response to conversation history
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            return ai_response
            
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"

# Create instance of our AI agent
agent = SimpleChatAgent()

print("Welcome to the Simple Chat Agent!")
print("Type 'quit' to exit")

while True:
    # Get user input
    user_input = input("\nYou: ")

    # Check if user wants to quit
    if user_input.lower() == 'quit':
        print("Goodbye!")
        break

    # Get and display AI response
    response = agent.get_response(user_input)
    print(f"AI: {response}")
