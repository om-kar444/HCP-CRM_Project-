from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "system",
            "content": """You are an assistant that extracts structured data from sales rep messages about HCP (doctor) interactions.
Extract the following fields and return ONLY valid JSON, nothing else, no markdown formatting, no code fences:
- hcp_name
- interaction_type (Meeting, Call, Email, Conference)
- topics_discussed
- sentiment (Positive, Neutral, Negative)
- materials_shared
- outcomes
- follow_up_actions
If a field is not mentioned, use null."""
        },
        {
            "role": "user",
            "content": "Met Dr. Sharma today, discussed OncoBoost Phase III data, she was neutral, wants more data before prescribing, gave her a brochure, need to send PDF"
        }
    ],
    temperature=0.3
)

print(response.choices[0].message.content)