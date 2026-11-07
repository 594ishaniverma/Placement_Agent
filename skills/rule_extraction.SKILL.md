# Rule extraction

Extract placement eligibility rules as structured JSON.

- Convert percentages and CGPA thresholds to numeric values.
- Preserve graduation year and branch restrictions.
- Keep placement status restrictions separate from academic rules.
- Never infer missing thresholds; leave them null.
- Return: `minimum_cgpa`, `minimum_tenth`, `minimum_twelfth`, `branches`,
  `graduation_year`, `maximum_backlogs`, `placed_status`.
