---
name: leadmagnet
description: Turn a useful topic into a practical lead magnet, three promotional post variations, and a portable HTML/PDF-ready deliverable.
---

# Lead Magnet Builder

Create a lead magnet that is specific enough to save the target audience real time.

## Step 1 — Gather inputs

Ask together when missing:

- What topic should the lead magnet cover?
- Who is the exact target audience?
- What should the reader be able to do afterward?
- Is there source material or proof that must be used?

Do not invent results, customer stories, statistics, or credentials.

## Step 2 — Choose the promise

Use a title that communicates a concrete outcome.

Useful patterns:

- The [Niche] [Playbook/Checklist]: [Specific Outcome]
- [Number] Steps to [Outcome] Without [Common Pain]
- How to [Outcome] When [Constraint]

Avoid vague “ultimate guide” language.

## Step 3 — Build the lead magnet

Create 5–7 concise sections. Each section needs:

- an action-oriented heading
- 2–3 concrete instructions
- one immediate action or checklist item

Include examples, templates, decision rules, or checklists when supported by the inputs.

## Step 4 — Write three promotional posts

### Post 1 — Contrarian

- Challenge a common belief.
- Explain the practical problem with it.
- Introduce the better approach.
- End with one CTA.

### Post 2 — Pain first

- Open with a specific frustrating situation.
- Explain why it keeps happening.
- Introduce the lead magnet as the shortcut.
- List three useful things inside.
- End with one CTA.

### Post 3 — Result or transformation

- Lead with a supported outcome or clear before/after state.
- Explain the mechanism briefly.
- Introduce the lead magnet.
- End with one CTA.

If no verified numeric result exists, use a concrete transformation instead of fabricating a number.

## Step 5 — Export

If the user provides an export destination or integration, use it.

Otherwise create a self-contained HTML file in the current working directory named from the title, for example:

```text
lead-magnet-title.html
```

The HTML should:

- use inline CSS only
- be responsive and readable
- have a maximum content width around 700px
- render headings, checklists, examples, and a simple footer
- print cleanly to PDF

Use the correct open command only when available:

```bash
# macOS
open "lead-magnet-title.html"

# Linux
xdg-open "lead-magnet-title.html"

# Windows
cmd.exe /c start "" "lead-magnet-title.html"
```

If opening fails, report the exact saved path and tell the user they can use Print → Save as PDF.

## Step 6 — Output

Return:

1. Lead magnet title and full content.
2. Three promotional posts.
3. Saved file path, if a file was created.
4. Any proof or source gaps that still need attention.
