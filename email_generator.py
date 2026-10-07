import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def generate_customer_email(rfq):

    prompt = f"""
Generate a professional customer email using ONLY the factual information
provided below.

IMPORTANT RULES:

- Do NOT invent any information.
- Do NOT make assumptions.
- Do NOT create commercial terms.
- Do NOT create delivery promises.
- Do NOT create payment terms.
- Do NOT create VAT information.
- Do NOT create discounts.
- Do NOT create warranties.
- Do NOT create certifications.
- Do NOT create quality-control information.
- Do NOT create tooling or setup costs.
- Do NOT create quote-validity periods.
- Do NOT create additional delivery schedules.
- Do NOT create company names, employee names, phone numbers or email addresses.
- Do NOT say that a delivery date can be met. Only state the requested date.
- Do NOT say that delivery is included unless explicitly stated below.
- Do NOT say that VAT is included or excluded.
- Do NOT mention anything that is not explicitly contained in the data below.

AVAILABLE FACTS:

Company:
{rfq["company"]}

Customer Email:
{rfq["email"]}

Product:
{rfq["product"]}

Quantity:
{rfq["quantity"]}

Requested Delivery Date:
{rfq["delivery_date"]}

Delivery Location:
{rfq["delivery_location"]}

Requirements:
{rfq["requirements"]}

Quoted Unit Price:
£{rfq["unit_price"]:,.2f}

Quoted Total Price:
£{rfq["total_price"]:,.2f}


EMAIL STRUCTURE:

Write a short professional email.

1. Thank the customer for their enquiry.
2. Confirm the product and quantity.
3. State the quoted unit price and total price.
4. If a delivery date exists, state it as a requested delivery date.
5. If a delivery location exists, state the delivery location.
6. Invite the customer to contact us if they have any questions.
7. End with "Kind regards,".

Do not add any information beyond the available facts.

Return ONLY the email body.

Do not use Markdown.
Do not include a subject line.
Do not use placeholders such as [Name], [Phone], or [Email].
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

    return response.choices[0].message.content.strip()