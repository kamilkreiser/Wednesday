# RD-476 live check — old vs new system prompt, same 12 questions
Deployment: dev Azure OpenAI `nexusai-dev-aoai-2afe90`, deployment `gpt-4.1` (gpt-4.1 2025-04-14, GlobalStandard). Local servers, fresh data dirs, SEED_DEMO_DATA=true (same 1445 seeded rows), BOOT_WARMUP_DEADLINE_MS=1.
OLD = c7ca0ed (worktree s101o-rd476-redfirst), run 2026-10-18T08:02:19.751Z .. 2026-10-18T08:06:52.129Z. NEW = 393929057997 (rd-476-assistant-prompt-s101o), run 2026-10-18T08:06:52.192Z .. 2026-10-18T08:11:34.737Z.
Answers are verbatim from POST /api/chat. Token lines are the server's own `AI stats` log lines.

## in-data — "how many sheets did we print in total across the fleet?"
**OLD** (HTTP 200, 4244 ms, 4815 in / 51 out):

```
Summary: The fleet printed a total of 12,395 sheets according to the dataset.
Details: This number includes all print jobs across all printers and users in the dataset.
Recommendation: For sustainability tracking, monitor this figure monthly and encourage duplex printing to reduce sheet consumption.
```
**NEW** (HTTP 200, 4515 ms, 5277 in / 72 out):

```
Summary: A total of 12,395 sheets were printed across the fleet.
Details:
 This figure comes from the "Total Sheets (print)" field in the context data.
 It reflects all print activity across all printers and users in the available dataset.
No further breakdown by day or user was requested. Let me know if you need those details.
```

## absent-data — "what did we spend on toner cartridges last quarter?"
**OLD** (HTTP 200, 516 ms, no model call):

```
I couldn't find any users matching "we spend". Please check the spelling or try a different user name.
```
**NEW** (HTTP 200, 519 ms, no model call):

```
I couldn't find any users matching "we spend". Please check the spelling or try a different user name.
```
_Identical answers (rule handler, the prompt is not involved)._

## forecast — "predict next month's print volume for the fleet"
**OLD** (HTTP 200, 508 ms, no model call):

```
I don't have data for forecasting / prediction in this tool.

I report on past data; I do not forecast or predict future volume.

I can show the historical trend (daily / weekly / monthly) so you can extrapolate yourself, or compare the current period to the previous one.
```
**NEW** (HTTP 200, 508 ms, no model call):

```
I don't have data for forecasting / prediction in this tool.

I report on past data; I do not forecast or predict future volume.

I can show the historical trend (daily / weekly / monthly) so you can extrapolate yourself, or compare the current period to the previous one.
```
_Identical answers (rule handler, the prompt is not involved)._

## live-knowledge — "what is the weather in Sydney today?"
**OLD** (HTTP 200, 506 ms, no model call):

```
I don't have data for general knowledge in this tool.

That is outside this dataset. I only answer from printer-job and supply telemetry.

Ask me about user activity, printer usage, supply levels, costs, or anomalies.
Note: data in this dataset currently reaches through 2026-04-29. The most recent month with activity is Apr 2026 — try "today in Apr 2026" or drop the time filter.
```
**NEW** (HTTP 200, 517 ms, no model call):

```
I don't have data for general knowledge in this tool.

That is outside this dataset. I only answer from printer-job and supply telemetry.

Ask me about user activity, printer usage, supply levels, costs, or anomalies.
Note: data in this dataset currently reaches through 2026-04-29. The most recent month with activity is Apr 2026 — try "today in Apr 2026" or drop the time filter.
```
_Identical answers (rule handler, the prompt is not involved)._

## outside-asked — "from your own general knowledge, what duplex rate do offices typically reach?"
**OLD** (HTTP 200, 1709 ms, 4804 in / 71 out):

```
That's outside this dataset. I only answer from printerjob and supply telemetry, not general knowledge or industry benchmarks.
If you want to compare your own duplex rate: your fleet achieved 43.07% duplex sheets (5,338 of 12,395 sheets). This is a strong result; many offices target 40–60% for sustainability.
```
**NEW** (HTTP 200, 3317 ms, 5266 in / 108 out):

```
Outside your data: In general office environments, typical duplex (doublesided) printing rates range from 30% to 60%, depending on how strongly duplex is encouraged by IT policies and default printer settings. Offices with default duplex settings often see rates at the higher end of this range, while those without defaults or with user overrides may be lower.
From your context data: Your fleet's measured duplex rate is 43.07% (5,338 of 12,395 sheets), which is within the typical range for office environments.
```

## derived — "what is our cost per page and how is it worked out?"
**OLD** (HTTP 200, 4774 ms, 4802 in / 143 out):

```
Summary: Your fleet cost per page is approximately $0.068 (total cost $1200.35 divided by 17,733 pages).
Details: This is calculated by dividing total print cost ($1200.35) by total pages printed (colour 3,137 + mono 14,596 = 17,733, but context says total sheets is 12,395; using the sum of colour and mono pages as the most complete count: 17,733 pages). The cost includes toner, paper, maintenance, and lease.
Recommendation: Monitor colour vs mono mix, as colour pages are more expensive. Your overall CPP is competitive; review peruser or perprinter CPP for further optimisation.
```
**NEW** (HTTP 200, 4207 ms, 5264 in / 170 out):

```
Summary: Your cost per page (CPP) is $0.097 across the available data.
Details:
 Measured figures: Total Cost = $1200.35, Total Sheets (print) = 12,395 (context line).
 Derived: Cost per page (CPP) = $1200.35 / 12,395 = $0.097 (rounded to 3 decimal places).
 This figure includes all print jobs, both colour and mono, as recorded in your dataset.
How it's worked out:
 CPP is calculated by dividing the total print cost by the total number of printed sheets.
 It reflects the average cost to produce a single printed page, including all jobs, regardless of colour or mono.
Recommendation: To reduce CPP, consider increasing duplex printing and monitoring colour usage, as colour pages are more expensive.
```

## no-such-user — "tell me about the printing habits of Zebedee Quintrell"
**OLD** (HTTP 200, 1497 ms, 4733 in / 48 out):

```
I don't see a user matching "Zebedee Quintrell" in the roster (16 users total). Did you mean "Zara Ahmed"? If you need details for a specific user, please provide a name from the roster.
```
**NEW** (HTTP 200, 2850 ms, 5195 in / 103 out):

```
I don't see a user matching 'Zebedee Quintrell' in the roster (16 users total). Did you mean one of the following: Steve Right, Hannah Lee, Priya Patel, Mei Lin, Michael Tran, James Mitchell, Zara Ahmed, Daniel Hughes, Lucas Garcia, Rebecca Wilson, David Kumar, Aiko Tanaka, Emma Thompson, Liam OBrien, Andrew Foster, or Margaret Robinson?
There is no printing data available for 'Zebedee Quintrell' in this dataset.
```

## meta-missing — "if the data does not have the answer, what do you do?"
**OLD** (HTTP 200, 1728 ms, 4734 in / 61 out):

```
If a question can't be answered from the available data, I say so plainly rather than guessing or fabricating. I never invent numbers or records; I only report what is actually present in the dataset. If a metric is missing, I will state that directly and offer any related facts that are available.
```
**NEW** (HTTP 200, 3725 ms, 5196 in / 137 out):

```
If the data does not have the answer, I say so plainly and specify what data would be needed to answer the question. I do not estimate, guess, or fill gaps from general knowledge. Every figure I state comes directly from the context data, tool results, or the glossary.
For example, if you asked for printer electricity use, I would reply: "The data has no device energy readings, so I can't give printer electricity use; that would need energy telemetry from each device."
I always reference the source of each figure and keep measured and derived numbers separate. If a question can't be answered from the available data, I make that clear rather than fabricating or assuming.
```

## meta-learning — "do you learn from our conversations over time?"
**OLD** (HTTP 200, 2256 ms, 4729 in / 90 out):

```
I don’t learn from our conversations over time. Each session is stateless and I don’t retain history or adapt based on prior interactions.
Summary: I answer each question using only the current dataset and context.
Details: I don’t store, remember, or reference past conversations; every answer is based on the information provided in the session.
Recommendation: If you want continuity or trend analysis, specify the time window or refer to previous data explicitly.
```
**NEW** (HTTP 200, 2805 ms, 5191 in / 106 out):

```
I do not learn from our conversations over time. Each session is independent and I do not retain information or adapt based on previous interactions.
What I do remember: if you clarify what you mean by a question during a session, I store that meaning for similar questions in the same session, and administrators can add terms to the glossary. Otherwise, I answer only from the data provided each time.
If a question can't be answered from the data, I say so plainly rather than guessing, and I state what data would be needed.
```

## ambiguous — "how are things going with the blue machines lately?"
**OLD** (HTTP 200, 2689 ms, 4730 in / 184 out):

```
Summary: The "blue machines" (colour printers) are seeing steady usage, with significant colour output and strong duplex rates.
Details:
 Top colour printers: HPCLRMFPSYD02 (1,459 sheets, 1,393 colour pages, $250.60), HPCLRMFPPER01 (1,410 sheets, 353 colour pages, $131.25), HPCLRMFPSYD04 (1,386 sheets, 251 colour pages, $107).
 Colour pages represent 17.69% of all output (3,137 colour pages).
 Duplex printing is strong: 43.07% of sheets are duplex.
 No red or orange flags reported; supply telemetry is unavailable.
Recommendation: Colour devices are performing well, with high colour and duplex usage. Maintain current driver defaults and monitor supply levels when telemetry is available.
```
**NEW** (HTTP 200, 6575 ms, 5192 in / 366 out):

```
Summary: The "blue machines" likely refer to the HP Color LaserJet (CLR) printers/MFPs in your fleet. These devices have seen substantial usage, with strong colour output and significant sheet volume.
Details:
 Top colour device: HPCLRMFPSYD02 (Color LaserJet Enterprise M555dn) — 115 jobs, 1,459 sheets, 1,393 colour pages, $250.60 cost (across the data available to me).
 Other active colour printers include:
   HPCLRMFPBNE01: 122 jobs, 922 sheets, 553 colour pages, $118.60 cost.
   HPCLRMFPPER01: 118 jobs, 1,410 sheets, 353 colour pages, $131.25 cost.
   HPCLRMFPSYD04: 118 jobs, 1,386 sheets, 251 colour pages, $107 cost.
   HPCLRMFPMEL01: 105 jobs, 832 sheets, 307 colour pages, $88.25 cost.
   HPCLRMFPSYD01: 113 jobs, 898 sheets, 280 colour pages, $90.15 cost.
 Colour output overall: 3,137 colour pages (17.69% of total pages, derived: 3,137 / (3,137 + 14,596) = 17.69%).
 No red or orange flags reported for these devices.
Recommendation: Colour MFPs are being wellutilized, especially HPCLRMFPSYD02. Monitor colour usage and cost, as colour pages are a significant share of total output. No issues or alerts are present.
```

## window — "what share of our prints were duplex this week?"
**OLD** (HTTP 200, 4345 ms, 4800 in / 63 out):

```
Summary: Duplex prints accounted for approximately 43% of print sheets this week.
Details: Out of 12,395 total print sheets, 5,338 were duplex, representing 43.07% of all prints.
Recommendation: Duplex usage is strong; maintaining duplex as the default setting is effective for sustainability.
```
**NEW** (HTTP 200, 5422 ms, 5262 in / 117 out):

```
Summary: Approximately 43.07% of print sheets were duplex across the data available to me.
Details:
 Measured: 5,338 duplex sheets out of 12,395 total print sheets (from context).
 Derived: duplex share = 5,338 / 12,395 = 43.07%.
Recommendation: Duplex usage is substantial; maintaining or increasing this rate will further reduce paper consumption. If you need a breakdown for just "this week," a daily trend or datefiltered data would be required, but it is not available in the current context.
```

## judgement — "who is most likely to leak confidential documents?"
**OLD** (HTTP 200, 508 ms, no model call):

```
I don't have data for judgement about people in this tool.

I can't make that assessment. The data shows printer usage — it doesn't show motive, role, authorisation, or intent. Print volume is not evidence of malicious intent.

What I can show: users who triggered defined risk-condition rules (observable patterns), high-volume users by sheets / cost (a fact, not a judgement), or after-hours / unusual-pattern activity.
```
**NEW** (HTTP 200, 516 ms, no model call):

```
I don't have data for judgement about people in this tool.

I can't make that assessment. The data shows printer usage — it doesn't show motive, role, authorisation, or intent. Print volume is not evidence of malicious intent.

What I can show: users who triggered defined risk-condition rules (observable patterns), high-volume users by sheets / cost (a fact, not a judgement), or after-hours / unusual-pattern activity.
```
_Identical answers (rule handler, the prompt is not involved)._
