from openai import OpenAI
import dotenv

dotenv.load_dotenv()

client = OpenAI()

response = client.responses.create(
    model="gpt-4.1",
    input="""
    write an essay about the importance of hydration for the human body
    use the following format:
    - introduction
    - body
    - conclusion
    - references
    - bibliography

    
    """
)

print(response.output_text)