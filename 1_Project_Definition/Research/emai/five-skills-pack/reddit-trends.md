---
name: reddit-trends
description: Find current audience discussions and recurring pain points on Reddit without requiring a Reddit API key.
---

# Reddit Trend Research

Use public Reddit data to identify current topics, questions, pain points, and content angles.

## Step 1 — Define the audience

Ask for:

- niche or audience
- geography, if relevant
- desired lookback window, defaulting to 30 days
- intended use: content, product research, lead magnet, or offer development

## Step 2 — Select communities

Choose 4–6 active, relevant subreddits. Prefer focused communities over massive generic ones.

Explain the selection briefly. Do not assume the example communities below are always correct.

Examples:

- Freelance / agency: `r/freelance`, `r/agency`, `r/smallbusiness`
- Marketing / content: `r/marketing`, `r/socialmedia`, `r/content_marketing`
- AI / automation: `r/artificial`, `r/ChatGPT`, `r/automation`, `r/LocalLLaMA`
- Fitness / coaching: `r/fitness`, `r/loseit`, `r/personaltraining`
- Career: `r/careerguidance`, `r/findapath`, `r/jobs`

## Step 3 — Collect public posts

For each subreddit, request the monthly top feed:

```bash
curl -s -H "User-Agent: PortableTrendResearch/1.0" "https://www.reddit.com/r/SUBREDDIT/top.json?t=month&limit=25"
```

Replace `SUBREDDIT` with the community name.

Extract:

- title
- score
- comment count
- permalink
- creation date

If Reddit blocks the request, use a browser or web-search tool available in the current environment. Do not ask for credentials merely to continue public research.

## Step 4 — Analyze

Look for:

- repeated problems across multiple posts
- questions appearing in different wording
- posts with unusually high comment counts
- objections, failed attempts, and tool complaints
- desired outcomes and buying signals

Separate genuine repeated patterns from one viral outlier.

## Step 5 — Report

Use this structure:

```markdown
# Trend Report — [Audience] — [Date Range]

## Top 5 Topics
1. [Topic] — [why it matters]

## Recurring Pain Points
- [Pain point]

## Questions People Keep Asking
- [Question]

## Content or Product Angles
1. [Specific angle] — Hook: “[opening line]”

## Strongest Opportunity
[One concise recommendation and why]

## Sources
- [Post title](permalink) — score/comments
```

Include source links. Do not present Reddit anecdotes as statistically representative research.

## Step 6 — Next action

Recommend one practical next step, such as:

- build a lead magnet from the strongest repeated pain point
- interview users about the highest-signal question
- draft three content angles
- test an offer against the most common failed workaround
