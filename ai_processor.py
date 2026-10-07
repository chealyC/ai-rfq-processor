import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def process_rfq(rfq_text):

    prompt = f"""
Extract the information from this RFQ.

Return ONLY valid JSON.
Do not include Markdown, explanations, or ```.

Use exactly these fields:

{{
    "company": "",
    "email": "",
    "product": "",
    "quantity": 0,
    "delivery_date": "",
    "delivery_location": "",
    "requirements": []
}}

If information is missing, use an empty string or empty list.

RFQ:
{rfq_text}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.choices[0].message.content

    return json.loads(result)