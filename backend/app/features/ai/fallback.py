from app.features.ai.prompts import (VALID_CATEGORIES, VALID_SEVERITIES)


FALLBACK_RESPONSES = {
    "accident": (
        "Exercise caution near the reported incident. "
        "Maintain a safe distance, avoid approaching potential "
        "hazards, and follow instructions from local authorities."
    ),
    "road_work": (
        "Reduce your speed when safe to do so and follow "
        "temporary traffic signs. Keep a safe distance from "
        "workers, machinery and restricted areas."
    ),
    "road_closure": (
        "Check available alternative routes and follow "
        "official diversion signs. Do not enter restricted "
        "areas or attempt to bypass road barriers."
    ),
    "pothole": (
        "Reduce your speed when safe to do so and remain "
        "alert to potential road surface defects. Avoid sudden "
        "manoeuvres that could endanger other road users."
    ),
    "traffic_light": (
        "Approach the reported junction cautiously. "
        "Follow applicable priority rules and traffic signs, "
        "and remain alert to pedestrians and other vehicles."
    ),
    "other": (
        "Exercise caution near the reported area. "
        "Maintain a safe distance from potential hazards "
        "and follow instructions from local authorities."
    ),
}


def get_fallback_advice(
    category: str,
    severity: str,
) -> str:

    if category not in VALID_CATEGORIES:
        raise ValueError("Invalid incident category.")

    if severity not in VALID_SEVERITIES:
        raise ValueError("Invalid incident severity.")

    advice = FALLBACK_RESPONSES[category]

    if severity == "high":
        advice += (
            " Avoid the reported area whenever it is "
            "safe and practical to do so."
        )

    return advice