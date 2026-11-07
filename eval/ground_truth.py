from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from agent.nodes.extract_rules import extract_rules
from mcp_server.tools import query_eligible_students


def expected_students(post_text: str) -> list[str]:
    rules = extract_rules(post_text)
    filters = {}
    mapping = {
        "minimum_cgpa": ("cgpa", "gte"),
        "minimum_tenth": ("tenth_percent", "gte"),
        "minimum_twelfth": ("twelfth_percent", "gte"),
        "graduation_year": (None, "eq"),
        "maximum_backlogs": ("backlogs", "lte"),
        "placed_status": (None, "eq"),
    }
    for rule_name, (column, operator) in mapping.items():
        value = rules.get(rule_name)
        if value is None:
            continue
        column = column or rule_name.replace("minimum_", "")
        if rule_name == "graduation_year":
            column = "graduation_year"
        if rule_name == "placed_status":
            column = "placed"
        filters[column] = value if operator == "eq" else {"operator": operator, "value": value}
    candidates = query_eligible_students(filters, limit=500)
    branches = {branch.upper() for branch in rules.get("branches", [])}
    if branches:
        candidates = [row for row in candidates if row["branch"].upper() in branches]
    return sorted(row["student_id"] for row in candidates)


def expected_ambiguity(post_text: str) -> bool:
    lower = post_text.lower()
    return "vague" in lower or "good academic" in lower or "acceptable academic" in lower or bool(
        re.search(r"\b(?:or|and/or)\b", lower)
    ) or len(set(re.findall(r"(\d+(?:\.\d+)?)\s*(?:cgpa|gpa)", lower))) > 1
