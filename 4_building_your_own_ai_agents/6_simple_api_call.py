import openai
import json
from MyKey import MY_OPENAI_KEY # Replace with your actual OpenAI API key in MyKey.py

# Initialize OpenAI client
client = openai.OpenAI(api_key=MY_OPENAI_KEY)  # Replace with your actual API key

# Define the Python function to add two numbers
def add_numbers(a, b):
    print(f"Calling add_numbers() function for {a} and {b}")
    return a + b

# Define the function specification for OpenAI
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_numbers",
            "description": "Adds two numbers together and returns the sum.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "The first number"},
                    "b": {"type": "number", "description": "The second number"}
                },
                "required": ["a", "b"]
            }
        }
    }
]

def chat_with_function_calling(user_input):
    # Send the message to OpenAI with function calling enabled
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # You can use "gpt-4" or other models if available
        messages=[{"role": "user", "content": user_input}],
        tools=tools,
        tool_choice="auto"  # Let the model decide whether to call the function
    )

    # Get the response message
    message = response.choices[0].message

    # Check if the model wants to call a function
    if message.tool_calls:
        for tool_call in message.tool_calls:
            if tool_call.function.name == "add_numbers":
                # Parse the arguments from the function call
                args = json.loads(tool_call.function.arguments)
                a = args["a"]
                b = args["b"]

                # Call the Python function
                result = add_numbers(a, b)

                # Send the result back to OpenAI for a final response
                final_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "user", "content": user_input},
                        message,  # Include the tool call
                        {
                            "role": "tool",
                            "content": str(result),
                            "tool_call_id": tool_call.id
                        }
                    ]
                )
                return final_response.choices[0].message.content
    else:
        # If no function call, return the model's direct response
        return message.content

print("Welcome! Ask me to add numbers or chat normally. Type 'quit' to exit.")
while True:
    user_input = input("\nYou: ")
    if user_input.lower() == 'quit':
        print("Goodbye!")
        break
    response = chat_with_function_calling(user_input)
    print(f"AI: {response}")