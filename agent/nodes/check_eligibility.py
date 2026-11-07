from mcp_server.tools import query_eligible_students


def check_eligibility(rules: dict) -> list[dict]:
    filters = {}
    if rules.get("minimum_cgpa") is not None:
        filters["cgpa"] = {"operator": "gte", "value": rules["minimum_cgpa"]}
    if rules.get("minimum_tenth") is not None:
        filters["tenth_percent"] = {"operator": "gte", "value": rules["minimum_tenth"]}
    if rules.get("minimum_twelfth") is not None:
        filters["twelfth_percent"] = {"operator": "gte", "value": rules["minimum_twelfth"]}
    if rules.get("graduation_year") is not None:
        filters["graduation_year"] = rules["graduation_year"]
    if rules.get("maximum_backlogs") is not None:
        filters["backlogs"] = {"operator": "lte", "value": rules["maximum_backlogs"]}
    if rules.get("placed_status") is not None:
        filters["placed"] = rules["placed_status"]
    candidates = query_eligible_students(filters, limit=500)
    branches = {branch.upper() for branch in rules.get("branches", [])}
    if branches:
        candidates = [student for student in candidates if student["branch"].upper() in branches]
    return candidates
