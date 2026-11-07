import re
from typing import Any


def extract_rules(post_text: str) -> dict[str, Any]:
    text = post_text.lower()
    rules: dict[str, Any] = {
        "minimum_cgpa": None,
        "minimum_tenth": None,
        "minimum_twelfth": None,
        "branches": [],
        "graduation_year": None,
        "maximum_backlogs": None,
        "placed_status": None,
    }
    match = re.search(r"(?:cgpa|gpa).*?(?:at least|minimum)?\s*(\d+(?:\.\d+)?)", text)
    if match:
        rules["minimum_cgpa"] = float(match.group(1))
    match = re.search(r"(?:10th|class x|tenth).*?(?:at least|minimum)?\s*(\d+(?:\.\d+)?)\s*%?", text)
    if match:
        rules["minimum_tenth"] = float(match.group(1))
    match = re.search(r"(?:12th|class xii|twelfth).*?(?:at least|minimum)?\s*(\d+(?:\.\d+)?)\s*%?", text)
    if match:
        rules["minimum_twelfth"] = float(match.group(1))
    match = re.search(r"\b(20\d{2})\b", text)
    if match:
        rules["graduation_year"] = int(match.group(1))
    branches = [branch for branch in ("cse", "it", "ece", "mechanical", "eee") if re.search(rf"\b{branch}\b", text)]
    rules["branches"] = branches
    match = re.search(r"(?:no more than|maximum|max).*?(\d+).*?(?:backlog|arrear)", text)
    if match:
        rules["maximum_backlogs"] = int(match.group(1))
    if "not placed" in text or "unplaced" in text:
        rules["placed_status"] = 0
    return rules
