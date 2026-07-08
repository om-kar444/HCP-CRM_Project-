from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

EXTRACTION_SYSTEM_PROMPT = """You are an assistant that extracts structured data from sales rep messages about HCP (doctor) interactions.
Extract the following fields and return ONLY valid JSON, nothing else, no markdown formatting, no code fences:
- hcp_name
- interaction_type (Meeting, Call, Email, Conference)
- topics_discussed
- sentiment (Positive, Neutral, Negative)
- materials_shared (brochures, documents, PDFs shared with the HCP)
- samples_distributed (drug samples, vials, or medical samples given to HCP)
- outcomes
- follow_up_actions
If a field is not mentioned, use null."""

EDIT_SYSTEM_PROMPT = """You are an assistant that identifies what a sales rep wants to change about a previously logged HCP interaction.
Given the rep's correction message, return ONLY valid JSON, nothing else, no markdown formatting, no code fences.
Return JSON with these possible keys (only include keys that are actually being changed):
- hcp_name
- interaction_type
- topics_discussed
- sentiment
- outcomes
- follow_up_actions
Only include the fields the rep is asking to change. Do not include fields not mentioned."""

FOLLOWUP_SYSTEM_PROMPT = """You are an assistant that suggests follow-up actions for a pharma sales rep based on a logged HCP interaction.
Given the interaction details, return ONLY a valid JSON array of 2-3 short, specific follow-up suggestions, nothing else, no markdown formatting.
Example output: ["Send Phase III trial PDF", "Schedule follow-up meeting in 2 weeks", "Add to advisory board invite list"]"""

COMPLIANCE_SYSTEM_PROMPT = """You are a pharma compliance assistant. Review the sales rep's interaction message for any statements that could violate pharmaceutical marketing compliance rules (e.g. promising off-label use, guaranteeing outcomes, making unapproved medical claims, offering improper incentives).
Return ONLY valid JSON, nothing else, no markdown formatting, in this exact format:
{"flagged": true or false, "reason": "short explanation or null if not flagged"}"""

HISTORY_SUMMARY_PROMPT = """You are an assistant that summarizes a sales rep's interaction history with a doctor.
Given a list of past interactions, write a short, natural 2-3 sentence summary of the relationship and key points discussed.
Return ONLY plain text, no JSON, no markdown."""


def extract_interaction_data(message: str) -> dict:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": EXTRACTION_SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ],
        temperature=0.3
    )
    return json.loads(response.choices[0].message.content)


def extract_edit_data(message: str) -> dict:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": EDIT_SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ],
        temperature=0.3
    )
    return json.loads(response.choices[0].message.content)


def generate_followup_suggestions(interaction_summary: str) -> list:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": FOLLOWUP_SYSTEM_PROMPT},
            {"role": "user", "content": interaction_summary}
        ],
        temperature=0.5
    )
    return json.loads(response.choices[0].message.content)


def check_compliance(message: str) -> dict:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": COMPLIANCE_SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ],
        temperature=0
    )
    return json.loads(response.choices[0].message.content)


def summarize_history(history_text: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": HISTORY_SUMMARY_PROMPT},
            {"role": "user", "content": history_text}
        ],
        temperature=0.4
    )
    return response.choices[0].message.content.strip()


def classify_message_intent(message: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """Classify the sales rep's message into exactly ONE of these categories:
- "log" - describing a new HCP interaction that just happened
- "edit" - correcting/changing something previously logged (e.g. "actually change...", "update...", "no wait...")
- "history" - asking about past interactions with an HCP (e.g. "what did I discuss with Dr. X last time", "show history")
- "followup" - asking for follow-up suggestions (e.g. "what should I do next", "suggest follow-up")
- "compliance" - asking to check if something is compliant/risky (e.g. "is this okay to say", "check compliance")
Return ONLY the single word: log, edit, history, followup, or compliance"""
            },
            {"role": "user", "content": message}
        ],
        temperature=0
    )
    intent = response.choices[0].message.content.strip().lower()
    valid = ["log", "edit", "history", "followup", "compliance"]
    for v in valid:
        if v in intent:
            return v
    return "log"