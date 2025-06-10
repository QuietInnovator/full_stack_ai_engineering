import openai
import os
import json
from openai import OpenAI
import dotenv

dotenv.load_dotenv()

# Set your API key (you can also use environment variable: os.getenv("OPENAI_API_KEY"))
client = OpenAI()

# --- Tool function: used by you, not the model ---
def multiply_numbers(a: int, b: int) -> int:
    print(f"🔧 Tool called with: a={a}, b={b}")
    return a * b

# --- Tool (function) schema ---
tool_definition = {
    "type": "function",
    "function": {
        "name": "multiply_numbers",
        "description": "Multiplies two integers and returns the result.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "integer", "description": "First number"},
                "b": {"type": "integer", "description": "Second number"}
            },
            "required": ["a", "b"]
        }
    }
}

# --- Prompt for the model ---
initial_prompt = """
You are a precise and persistent assistant.

Task: Multiply two numbers using the tool provided. Never guess the result—always call the tool to compute it.

Guidelines:
- Plan your approach before taking action.
- Always use tools when available.
- After calling a tool, reflect on the result to confirm correctness.
- Do not stop until you have used the tool and confirmed a correct result.

Now, multiply 5678 and 8765.
"""

# Step 1: Initial ChatCompletion call with tool definitions
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a thoughtful assistant who always uses tools to solve problems."},
        {"role": "user", "content": initial_prompt}
    ],
    tools=[tool_definition],
    tool_choice="auto"
)

message = response.choices[0].message
tool_call = message.tool_calls[0]
args = json.loads(tool_call.function.arguments)

# Step 2: Call your own local tool
result = multiply_numbers(args["a"], args["b"])

# Step 3: Send the tool result back to the model for reflection
followup_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a thoughtful assistant who always reflects after using a tool."},
        {"role": "user", "content": initial_prompt},
        message,
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": tool_call.function.name,
            "content": str(result)
        }
    ]
)


# Step 4: Print final response
print("\n🤖 Final Assistant Response:")
print(followup_response.choices[0].message.content)
