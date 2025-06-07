import openai


def get_response(prompt, openai_api_key):
    client = openai.OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def add(a, b, openai_api_key):
    return get_response(f"Add {a} and {b}, and return the result as a number.", openai_api_key)

def subtract(a, b, openai_api_key):
    return get_response(f"Subtract {b} from {a}, and return the result as a number.", openai_api_key)

def multiply(a, b, openai_api_key):
    return get_response(f"Multiply {a} and {b}, and return the result as a number.", openai_api_key)

def divide(a, b, openai_api_key):
    return get_response(f"Divide {a} by {b}, and return the result as a number.", openai_api_key)
