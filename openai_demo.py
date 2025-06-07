import openai

client = openai.OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Tell me a joke about sloths."}
    ],
)

print(response.choices[0].message.content)