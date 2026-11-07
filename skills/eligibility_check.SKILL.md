# Eligibility check

Apply extracted rules conservatively:

1. Start from the allowlisted `students` table.
2. Apply one conjunctive condition for every explicit rule.
3. If a value is missing or conflicting, do not guess.
4. Return student IDs and never include phone numbers, private email addresses,
   or unrelated fields in a notice.
