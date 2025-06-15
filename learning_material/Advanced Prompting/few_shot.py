from openai import OpenAI
import dotenv

dotenv.load_dotenv()

client = OpenAI()

# zero shot
response = client.responses.create(
    model="gpt-4.1",
    input="""
Summarize the following review in one helpful sentence: "I've been using this coffee grinder for a month and I love the consistent grind size. It's a bit noisy, but overall worth the price."    
    """
)

print("zero shot result: ", response.output_text)

# few shot

response = client.responses.create(
    model="gpt-4.1",
    input="""
Summarize each product review in one sentence that captures the main pros and cons:

Review: "This vacuum is light and easy to use, but battery life could be better."
Summary: "Lightweight and user-friendly vacuum with limited battery life."

Review: "The keyboard feels great to type on and the battery lasts all day."
Summary: "Excellent typing experience with outstanding battery life."

Review: "I've been using this coffee grinder for a month and I love the consistent grind size. It's a bit noisy, but overall worth the price."
Summary:
    """
)

print("few shot result: ", response.output_text)