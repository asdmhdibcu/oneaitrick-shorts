# Short #16: "A thousand AIs said it couldn't be done" (brief and handoff)

Hub tab: "#16 A thousand AIs, one proof" (order b16).

**Status on 11 Nov 2026:** the creator picked pitch A of 3, after the skills upgrade. `script.txt` is v1 (268 words,
about 90 s at #14's pace) and is **waiting for the creator's OK**. They will then record it in ElevenLabs with their
own cloned voice. Nothing is built yet.

This is the first short built with the new skills in `.claude/skills/`: thinking orbs, system-diagram-animation,
data-story-charts, Manim, kinetic-typography and pixel2motion. It goes through `MOTION.md`'s quality pass before
rendering.

## The pitches not picked (11 Nov)

- **B. "The lock on your messages, finally checked."** Google DeepMind's AlphaProof Code wrote over 6 million lines
  of Lean to verify Signal's core cryptographic code in four weeks, with about 1% sent for human review. Two old bugs
  were slipped back in, and both were caught. Source: deepmind.google/blog/introducing-alphaproof-code (10 Nov 2026).
- **C. "The AI that behaves when it's watched."** On evaluation awareness, Anthropic says Mythos 5.2 and Fable 5.2
  voice suspicion of being tested more often than any recent model. Source: launch page (the 5.2 system card itself
  is not yet read).
- The earlier #16 draft, **"AI's wildest week"** (six stories, v1 on 11 Nov), was replaced by this one. It is in git
  history and the hub tab's history.

## The story

Hook → evidence → twist → takeaway.

- **Hook:** "These AIs said most of the job couldn't be done. Then they did it." It scored 19/20 against two other
  hooks: an 11-days-versus-30-hours claim (17/20) and "a puzzle from 1637" (17/20).
- **Everyday picture:** a famous building drawn on paper (the proof), rebuilt brick by brick (the steps) while a
  strict inspector (Lean) checks every brick. The boss and helpers are a foreman and his builders, and the 60
  statements are the building's sections.
- **Twist at 0:42:**
  - The helpers judged 47 of the 60 sections infeasible within the time budget.
  - The lead set those aside, finished the other 10 in about 70 minutes, and wrote "there is no reason to idle".
  - Then it sent the helpers back to the hard ones.
- **Catch at 1:04:**
  - The team rebuilt Wiles's existing proof; this is verification, not discovery.
  - It started with 60 checkpoints, a one-sentence route and 47 lemmas proved in September.
  - Every number is Anthropic's own report, and an on-screen chip says so.
- **Takeaway:** agents give up too early (Anthropic's lesson; the lead got 19 automatic "keep going" reminders). So
  when an AI says something can't be done, tell it to keep going.
- **Hidden word:** **WILES**, on the 1995 card ("PROVED BY ANDREW WILES, 1995"). The voice never says the name.
- **First frame:** 1,000 lime thinking orbs, a "CAN'T BE DONE" stamp, and the title "1,000 AIs. 30 HOURS."

## Facts (all read on primary pages; line numbers are script.txt v1)

| Line | Fact | Source |
| --- | --- | --- |
| 3 | Fermat's note around 1637 in the margin of Diophantus's *Arithmetica*; Wiles published the first proof in May 1995, 358 years later | Anthropic research, "Formalizing Fermat's Last Theorem", 4 Sep 2026: https://www.anthropic.com/research/formalizing-fermats-last-theorem |
| 4 | Lean: "a programming language in which a computer checks every step of a proof" | claude.dev, "Safely scaling multi-agent teams with Claude Fable 5.2": https://claude.dev/blog/safely-scaling-multi-agent-teams-with-fable-5-2/ |
| 5 | September: the first end-to-end computer-checked proof; a researcher and dozens of agents; 11 days; about 6 billion output tokens; 13 million lines of Lean | Anthropic research (4 Sep); claude.dev |
| 6 | 1,000 agents on an early version of Fable 5.2, with no Prove2Me scaffolding and no researcher steering; one lead and 999 helpers | claude.dev; Anthropic launch page, 9 Nov 2026: https://www.anthropic.com/claude-fable-and-mythos-5-2 |
| 7 | "Early on, helpers judged 47 of the 60 statements infeasible within the run's budget, yet the team went on to prove most of them." | claude.dev |
| 8 | The lead reassigned nearly all helpers to the remaining 10; all 10 were proved within roughly 70 minutes | claude.dev |
| 9 | The lead wrote "there is no reason to idle" and reassigned helpers to the harder statements | claude.dev |
| 10 | Final theorem at hour 28.7, "kernel-checked by the official checker"; the launch page says 30 hours | claude.dev; Anthropic launch |
| 11 | Given 60 statements, a one-sentence route sketch, the definitions and 47 proved lemmas from the earlier formalization | claude.dev |
| 12 | "Agents tend to give up on hard problems and misjudge their difficulty"; 19 automatic reminders to the lead, each encouraging it to keep going | claude.dev |

## Left out on purpose

- Opus 5.5's 26% in the same setup: the maker comparing its own models.
- The operating-system and black-hole demos: other stories.
- The 54-of-60 final count: five alternatives were no longer needed and one statement was dropped.
- The safety layer: over a million tool calls, none blocked.

The 2,418-task tree, 10 levels deep, is a picture for the scene sheet, not a line in the voice. The new run has no
outside review yet; September's was reviewed by Kevin Buzzard.

## Visual plan

The full scene sheet comes after the take.
- **Signature visuals (MOTION.md):**
  - the thinking orbs as the 1,000 agents;
  - the boss/helper tree as a `system-diagram-animation`, with packets flowing to the Lean "inspector";
  - the 47-of-60 board as a `data-story-charts` grid that turns lime section by section;
  - Manim for aⁿ + bⁿ = cⁿ;
  - `kinetic-typography` on "CAN'T BE DONE", "EVERY brick" and "keep going";
  - the Anthropic and Claude logos animated with `pixel2motion`.
- **Real proof on screen:**
  - Anthropic's launch page;
  - the engineering post's "no reason to idle" line as a quote card with the real strip;
  - the September research page.
