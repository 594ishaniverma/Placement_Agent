from agent.guardrails import contains_private_field, guard_notice, validate_student_ids


def test_private_fields_are_detected():
    assert contains_private_field("Email is required")
    assert contains_private_field("Call the phone number")
    assert not contains_private_field("Apply through the placement portal")


def test_unknown_student_is_rejected():
    safe, errors = guard_notice("Placement notice for eligible students.", ["UNKNOWN-ID"])
    assert not safe
    assert errors


def test_validation_filters_unknown_ids():
    assert validate_student_ids(["UNKNOWN-ID"]) == []
