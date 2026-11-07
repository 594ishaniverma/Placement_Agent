def human_approval(draft: str) -> tuple[bool, str]:
    print("\n--- Draft notice ---")
    print(draft)
    print("--------------------")
    while True:
        answer = input("Approve notice? [y/N]: ").strip().lower()
        if answer in {"y", "yes"}:
            return True, draft
        if answer in {"", "n", "no"}:
            return False, draft
