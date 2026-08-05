---
name: skill-creator
description: Create or update a portable, self-contained skill for the user's current AI agent or coding harness.
---

# Skill Creator

Create reusable skills without assuming a specific computer, username, vault, or global configuration.

## Step 1 — Define the skill

Ask only for information that is missing:

1. Skill name and trigger.
2. What it should accomplish.
3. Expected inputs and outputs.
4. Files or tools it may read.
5. Files or tools it may modify.
6. Actions that require user approval.
7. How success should be validated.

## Step 2 — Inspect the current project

Before inventing a location:

- Check the current agent’s documentation or existing project conventions.
- Look for an existing project-level skills directory.
- Reuse the structure already present.
- Prefer project-relative paths.

If no skill system exists, create a standalone Markdown skill file in a clearly named project folder and explain how to invoke it manually.

Do not install dependencies, change global configuration, or write outside the current project without approval.

## Step 3 — Design the workflow

The skill should include:

- YAML frontmatter with `name` and `description`
- a clear goal
- required inputs
- numbered execution steps
- allowed tools and writes
- stop/approval gates
- validation checks
- expected output format

Keep the workflow self-contained. If it depends on another file, use a path relative to the skill folder or current project and include that dependency in the package.

## Step 4 — Write the skill

Use the current harness’s expected filename and folder structure.

Common project-level shape:

```text
<your-project>/
  <skills-directory>/
    <skill-name>/
      SKILL.md
```

Never hardcode examples such as a personal home directory, drive letter, username, or another person’s vault path.

## Step 5 — Validate portability

Before finishing, scan the new skill for:

- absolute drive-letter paths
- personal macOS home-directory paths
- personal Linux home-directory paths
- references to files not included in the project
- secret values or tokens
- destructive or external actions without approval gates

Fix every portability issue found.

## Step 6 — Report

Return:

- skill path
- trigger/invocation
- included dependencies
- validation performed
- any setup the user still needs to complete
