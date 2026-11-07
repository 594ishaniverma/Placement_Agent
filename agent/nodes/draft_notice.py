from agent.prompts import load_skill


def draft_notice(post_name: str, rules: dict, eligible_count: int, ambiguous: bool) -> str:
    load_skill("notice_drafting.SKILL.md")
    role = post_name.replace("_", " ").replace("-", " ")
    requirements = []
    if rules.get("minimum_cgpa") is not None:
        requirements.append(f"CGPA >= {rules['minimum_cgpa']:.1f}")
    if rules.get("minimum_tenth") is not None:
        requirements.append(f"Class X >= {rules['minimum_tenth']:.0f}%")
    if rules.get("minimum_twelfth") is not None:
        requirements.append(f"Class XII >= {rules['minimum_twelfth']:.0f}%")
    if rules.get("branches"):
        requirements.append("Branches: " + ", ".join(branch.upper() for branch in rules["branches"]))
    summary = "; ".join(requirements) or "as specified in the placement post"
    notice = (
        f"Placement Notice: {role}\n"
        f"Eligibility: {summary}.\n"
        f"{eligible_count} eligible students are currently identified.\n"
        "Apply through the placement portal.\n"
        "Human approval required before circulation."
    )
    if ambiguous:
        notice += "\nAmbiguity detected: placement office review is required."
    return notice
