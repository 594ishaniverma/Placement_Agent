import re
from typing import Any


def detect_ambiguity(post_text: str, rules: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons = []
    lower = post_text.lower()
    if "cgpa" not in lower and "gpa" not in lower:
        reasons.append("No CGPA requirement is stated.")
    if re.search(r"\b(or|and/or)\b", lower):
        reasons.append("The post contains an ambiguous OR rule.")
    values = re.findall(r"(\d+(?:\.\d+)?)\s*(?:cgpa|gpa)", lower)
    if len(values) > 1 and len(set(values)) > 1:
        reasons.append("Conflicting CGPA requirements are present.")
    if not rules.get("branches"):
        reasons.append("No branch restriction is stated.")
    return bool(reasons), reasons
