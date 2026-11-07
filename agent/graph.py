from agent.guardrails import guard_notice
from agent.nodes.check_eligibility import check_eligibility
from agent.nodes.detect_ambiguity import detect_ambiguity
from agent.nodes.draft_notice import draft_notice
from agent.nodes.extract_rules import extract_rules
from agent.nodes.human_approval import human_approval
from agent.state import PlacementState


def run_workflow(post_name: str, post_text: str, interactive: bool = True) -> PlacementState:
    rules = extract_rules(post_text)
    ambiguous, reasons = detect_ambiguity(post_text, rules)
    students = check_eligibility(rules) if not ambiguous else check_eligibility(rules)
    notice = draft_notice(post_name, rules, len(students), ambiguous)
    safe, errors = guard_notice(notice, [student["student_id"] for student in students])
    if not safe:
        notice += "\nGuardrail warning: " + " ".join(errors)
        approved = False
    elif interactive:
        approved, notice = human_approval(notice)
    else:
        approved = False
    return {
        "post_name": post_name,
        "post_text": post_text,
        "rules": rules,
        "ambiguous": ambiguous,
        "ambiguity_reasons": reasons,
        "students": students,
        "draft": notice,
        "approved": approved,
    }
