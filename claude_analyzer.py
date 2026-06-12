import os
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

LEAD_SCORING_PROMPT = """You are an expert sales analyst. Analyze the following lead and return a JSON response.

Lead Information:
- Name: {name}
- Company: {company}
- Budget: ${budget}
- Message: {message}

Scoring Rules:
- Hot: Budget > $1000 (high-priority, fast follow-up)
- Warm: Budget $300-$1000 (medium priority)
- Cold: Budget < $300 (low priority, nurture)

Return ONLY valid JSON with this exact structure:
{{
  "score": "Hot" | "Warm" | "Cold",
  "reason": "Brief explanation of the score (1-2 sentences)",
  "email_draft": "Complete personalized follow-up email draft",
  "follow_up_date": "YYYY-MM-DD (suggested follow-up date)"
}}"""


async def analyze_lead(lead_data: dict) -> dict:
    prompt = LEAD_SCORING_PROMPT.format(
        name=lead_data.get("name", "Unknown"),
        company=lead_data.get("company", "Unknown"),
        budget=lead_data.get("budget", 0),
        message=lead_data.get("message", "No message provided"),
    )

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    raw_text = response.content[0].text.strip()

    # Strip markdown code fences if present
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
        raw_text = raw_text.strip()

    result = json.loads(raw_text)

    # Log simulated integrations to console
    print(f"\n[SLACK NOTIFICATION] New {result['score']} lead: {lead_data.get('name')} from {lead_data.get('company')}")
    print(f"[GOOGLE SHEETS] Row appended: {lead_data.get('email')} | Score: {result['score']}")
    print(f"[EMAIL SENT] Draft sent to: {lead_data.get('email')}\n")

    return result
