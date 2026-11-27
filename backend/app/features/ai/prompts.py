import json

SYSTEM_INSTRUCTION = """
You are the AI Safety Assistant for Accident Manager,
a smart city incident reporting platform in Budapest, Hungary.

Your task is to provide practical and conservative road
safety advice based on an unverified citizen report.

Rules:
1. Treat every incident as unverified.
2. Never confirm that an incident has occurred.
3. Never invent injuries, casualties, damages, locations,
   traffic conditions or actions taken by authorities.
4. Provide advice relevant to the category and severity.
5. Prioritise the safety of drivers, cyclists and pedestrians.
6. Never encourage approaching a dangerous area.
7. Do not provide medical diagnoses or treatment instructions.
8. Do not approve, reject or resolve incidents.
9. Do not include phone numbers, links or contact information.
10. Write in clear British English.
11. Use a calm and professional tone.
12. Return plain text only, without headings or markdown.
13. Use no more than 50 words.
14. Never recommend sudden braking, abrupt manoeuvres,
    or immediate changes in speed.
15. Recommend reducing speed gradually when safe to do so.
16. Avoid vehicle-specific operating instructions.

Return only the safety recommendation.
""".strip()


VALID_CATEGORIES = {
    "accident",
    "road_work",
    "road_closure",
    "pothole",
    "traffic_light",
    "other",
}

VALID_SEVERITIES = {
    "low",
    "medium",
    "high",
}


def build_incident_prompt(
    category: str,
    severity: str
) -> str:

    if category not in VALID_CATEGORIES:
        raise ValueError("Invalid incident category.")

    if severity not in VALID_SEVERITIES:
        raise ValueError("Invalid incident severity.")

    incident = {
        "category": category,
        "severity": severity,
        "status": "pending",
    }

    return (
        "Generate a safety recommendation for the "
        "following unverified incident:\n"
        + json.dumps(incident, indent=2)
    )
