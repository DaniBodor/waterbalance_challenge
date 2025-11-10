AI_USAGE.md — How I used AI tools in this exercise

Instructions

- Keep this file short (roughly 0.5–1 page). Bullet points are fine.
- Do not paste secrets, company‑internal or proprietary text into AI tools.
- This exercise runs offline; no external API calls are required.

1. Tools used

- Copilot

2. Prompt(s)

- remove global state from codebase (removing global state from water model)
- refactor this into modular structure (refactor overly complex `run_all` function)

3. AI output kept vs. modified

- Global state removed kept.
- Add inline markers `# AI-ASSIST:` in code where the AI influenced your changes.

4. Manual correction or improvement (required)

- Removed beta altogether rather than mutiplying it with 0.
- Leaving a factor that is mutiplied by 0 hides the fact that this factor is unused, compared to not having it in the code base at all. If I want to later add it back in, I prefer having.
- It feels like the AI split it up too far into separate modules at first glance, but I do not have time to properly diagnose this in the last minutes before submitting the assignment. Or at least argument passing could be more efficient.

5. Reflection

- What went well? What misled you? What would you try differently next time?

---

Example (filled sample — for guidance)

Note: This is an example to illustrate expected content and depth. Replace with your own notes when you complete the exercise.

1. Tools used

- ChatGPT (web) for drafting ....
- GitHub Copilot in editor for ....

2. Prompt(s)

- Prompt 1 (to ChatGPT): "..."
- Prompt 2 (to ChatGPT): "..."

3. AI output kept vs. modified

- Kept: ...
- Modified: ...
- Marked in code with `# AI-ASSIST:` near the relevant function/test.

4. Manual correction or improvement (required)

- AI suggested .... in one draft. I corrected this to ....

5. Reflection

- Went well: Using AI to .... saved time; only good starting for .... but needed manual changes to ....
- Misleading: The first suggestion for .... was misleading but by ..... I was able to get the right answer.
