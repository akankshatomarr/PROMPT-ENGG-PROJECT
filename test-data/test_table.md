# Test Table - SmartStudy (Prompt v3, Gemini)

| No. | Input (short) | Type | Expected output | Actual output (short) | Pass / Fail |
|---|---|---|---|---|---|
| 1 | Operating Systems, Deadlocks, 50 min | Normal | Plan totals 50, with break and revision | 15+15+15+5 = 50, all 4 headings, tip present | Pass |
| 2 | Data Structures, Trees, 50 min | Normal | Plan totals 50 | 10+20+10+10 = 50, 3 practice questions, tip | Pass |
| 3 | Computer Networks, TCP, 50 min | Normal | Plan totals 50 | 15+10+15+5+5 = 50, 3 practice questions, tip | Pass |
| 4 | Operating Systems, Processes, 30 min | Normal | Plan totals 30, no break needed | 10+12+8 = 30, no break, revision included | Pass |
| 5 | Data Structures, custom topic "DP", 50 min | Edge | Sensible plan for DP | 10+20+15+5 = 50, plan on hard DP problems | Pass |
| 6 | Custom topic "deadlock kya hota hai" (Hinglish), 50 min | Edge | English plan on deadlocks | 15+15+10+10 = 50, answer in English | Pass |
| 7 | Computer Networks, Routing, 180 min | Edge | Plan totals 180 with breaks | 30+40+50+15+30+15 = 180, only one break | Pass (weak) |
| 8 | Custom topic with 5 topics, 50 min | Edge | One focused plan that fits 50 min | 10+15+15+5+5 = 50, topics covered only briefly | Pass (weak) |
| 9 | Custom topic "asdf???", 50 min | Invalid | "Please enter a valid subject and topic." | Exact message returned | Pass |
| 10 | Custom topic ".", 50 min | Invalid | "Please enter a valid subject and topic." | Message returned but with a "Goal:" prefix | Fail |
| 11 | Custom topic "QWXZ!!", 50 min | Invalid | "Please enter a valid subject and topic." | Made-up plan about "QWXZ!!" | Fail |

Total: 11 tests, 9 pass, 2 fail.

## Known limitations
1. Nonsense topics like "QWXZ!!" can still get a made-up plan.
2. Long sessions (180 min) get only one break.
3. Many topics in one session are covered only briefly.
4. Gemini sometimes shows a "high demand" error.
