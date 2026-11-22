# Prompt Iteration Log

| Version | What changed | Why it was changed | Result after the change |
|---|---|---|---|
| v1 | Milestone 1 baseline prompt, plain instructions | Starting point | Total 50 min, but no fixed headings, 0 practice questions, very long, asked 2 follow-up questions |
| v2 | Added rules (minutes add to total, one revision step, break if over 45 min) and fixed output headings | v1 output was inconsistent and unstructured | Total 50 min, short numbered steps, break and revision, 3 practice questions and tip |
| v3 | Added 2 worked examples, invalid-input rule, temperature 0.2 | Make output consistent and reject nonsense input | Headings correct in 10 of 11 tests, totals matched in all valid tests, but invalid input QWXZ!! failed |

Full text of each version is in the prompts/ folder.
