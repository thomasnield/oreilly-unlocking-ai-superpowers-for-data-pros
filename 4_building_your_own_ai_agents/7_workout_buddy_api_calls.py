import openai
from MyKey import MY_OPENAI_KEY # Replace with your actual OpenAI API key in MyKey.py

class WorkoutBuddy:
    def __init__(self):
        self.client = openai.OpenAI(api_key=MY_OPENAI_KEY)
        self.swing_count = 0
        self.getup_count = 0
        self.conversation_history = [
            {"role": "system",
             "content": """
             You are a helpful workout assistant to keep me motivated and track the user's sets. 
             The program is simple and sinister: 10 sets of kettlebell swings and then 10 Turkish get-ups. 
             The user will let you know when each set is done. 
             Use the provided functions to track counts: increment_swings() for swings, increment_getups() for get-ups, 
             get_swing_count() for current swing count, and get_getup_count() for current get-up count.
             Limit to two sentences and keep it brief, but motivational.
             """
             }
        ]

    def increment_swings(self):
        self.swing_count += 1
        print(f"called increment_swings(), swing_count now {self.swing_count}")
        return self.swing_count

    def increment_getups(self):
        self.getup_count += 1
        print(f"called increment_getups(), getup_count now {self.swing_count}")
        return self.getup_count

    def get_swing_count(self):
        print(f"called get_swing_count(), swing_count now {self.swing_count}")
        return self.swing_count

    def get_getup_count(self):
        print(f"called get_getup_count(), getup_count now {self.swing_count}")
        return self.getup_count

    def get_response(self, user_input):
        # Add user message to conversation history
        self.conversation_history.append({"role": "user", "content": user_input})

        # Define tools
        tools = [
            {"type": "function", "function": {"name": "increment_swings", "description": "Increments the kettlebell swing set count by 1.", "parameters": {"type": "object", "properties": {}}}},
            {"type": "function", "function": {"name": "increment_getups", "description": "Increments the Turkish get-up set count by 1.", "parameters": {"type": "object", "properties": {}}}},
            {"type": "function", "function": {"name": "get_swing_count", "description": "Returns the current number of kettlebell swing sets completed.", "parameters": {"type": "object", "properties": {}}}},
            {"type": "function", "function": {"name": "get_getup_count", "description": "Returns the current number of Turkish get-up sets completed.", "parameters": {"type": "object", "properties": {}}}}
        ]

        # First API call with tools
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.conversation_history,
            tools=tools,
            tool_choice="auto",
            max_tokens=1000,
            temperature=0.7
        )

        message = response.choices[0].message

        # Handle tool calls
        if message.tool_calls:
            # Append the assistant message with tool calls to history
            self.conversation_history.append(message)

            for tool_call in message.tool_calls:
                func_name = tool_call.function.name
                if func_name == "increment_swings":
                    result = self.increment_swings()
                elif func_name == "increment_getups":
                    result = self.increment_getups()
                elif func_name == "get_swing_count":
                    result = self.get_swing_count()
                elif func_name == "get_getup_count":
                    result = self.get_getup_count()

                # Append the tool result
                self.conversation_history.append({
                    "role": "tool",
                    "content": str(result),
                    "tool_call_id": tool_call.id
                })

            # Second API call with updated history
            final_response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=self.conversation_history,
                max_tokens=1000,
                temperature=0.7
            )
            assistant_response = final_response.choices[0].message.content.strip()
        else:
            assistant_response = message.content.strip()

        # Append final assistant response to history
        self.conversation_history.append({"role": "assistant", "content": assistant_response})
        return assistant_response

agent = WorkoutBuddy()
print("Welcome! Let's get to our workout! Type 'quit' to exit.")
while True:
    user_input = input("\nYou: ")
    if user_input.lower() == 'quit':
        print("Goodbye!")
        break
    response = agent.get_response(user_input)
    print(f"AI: {response}")