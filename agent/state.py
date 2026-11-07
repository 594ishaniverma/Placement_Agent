from typing import Any, TypedDict


class PlacementState(TypedDict, total=False):
    post_name: str
    post_text: str
    rules: dict[str, Any]
    ambiguous: bool
    ambiguity_reasons: list[str]
    students: list[dict[str, Any]]
    draft: str
    approved: bool
    corrections: list[str]
