# Short #10 — "The invisible signature" (brief and handoff)

Status on 24 Oct 2026, 02:05 UK: the creator picked this pitch (2 of 3). `script.txt` is draft v1, **waiting for the
creator's OK** before they record. It is 217 words, about 82 s at #9's pace (159 wpm with pauses). Nothing is built yet.

The other two pitches, not picked: "The AI that learned to talk by listening" (Block's Dessa, 23 Oct, full-duplex,
trained on speech only) and "Twenty Questions with a price tag" (Microsoft MAI-DxO, Science, 22 Oct, 83% vs 36%).

## The story

ChatGPT now invisibly watermarks its text in the EU. The everyday picture is a secret, loaded coin deciding each small
word choice ("big" or "large"). One word proves nothing; hundreds that follow the coin make a signature. Claude does
this worldwide, the UK included. The twist: Claude signs text it only translated, so your own words can carry it. The
catch: a mark is a signal, not proof, and teachers can't use ChatGPT's checker. The ending: if AI helped, say so,
because the words may already be saying it.

## Facts checked against primary pages (reachable from the workspace)

**OpenAI Help Center, "Provenance signals in OpenAI-generated content"**
(https://help.openai.com/en/articles/8912793-provenance-signals-in-openai-generated-content)
- In the EU, ChatGPT text carries an invisible change to the randomness in its word choices. The page names the EU
  only, never the UK. API customers worldwide can opt in; it is off by default.
- The mark is a secret key nudging word-choice probabilities. It adds no hidden characters. A detector holding the
  same key checks for the pattern.
- It is "designed to withstand common changes": light edits, copy-paste, screenshots. Heavy paraphrasing or
  translation can make it undetectable. Short passages are unreliable; the Code of Practice doesn't require marks
  under 200 tokens (about 150 English words) or on code.
- Test across the 24 EU languages (500 English prompts, translated): "At 1% false-positive rate, Spanish has the
  highest detection rate (69.0%), while Romanian has the lowest (42.2%)." OpenAI raised the strength for languages
  under 60%.
- Detector access is limited to approved research and academic organisations. "Academic integrity checks (such as
  checking student work)" are out of scope.
- OpenAI's own method is called textGrain; it plans to release it as open source.

**Claude Help Center, "How Claude marks AI-generated content"**
(https://support.claude.com/en/articles/16266773-how-claude-Marks-ai-generated-content)
- "Marking will apply to output from supported models wherever Claude is offered, worldwide." It covers models
  launched on or after 2 Aug 2026, with earlier ones being added.
- It "will travel with the text when it's copied and pasted elsewhere" and "may persist through some editing".
  Heavy edits, paraphrasing, translation and very short passages may defeat it.
- "People often use Claude to proofread, translate, summarize, or convert files", so marked output may not mean
  Claude wrote the content.
- "A detected mark provides a signal that content was processed by Claude, but is not fully conclusive."
- The detection API is in private preview for regulators, law enforcement, media, fact-checkers, independent
  researchers and educational organisations.

**Secondary sources only (not in the script):**
- 80% detection at about 200 tokens and 95% at about 400; 66% after swapping 10% of words (Trending Topics, 5 Oct,
  citing OpenAI's announcement).
- Anthropic's digits-of-pi key example (Engadget, 15 Aug).
- OpenAI announced on 5 Oct, rolling out "in the coming weeks".

**Unreachable from the workspace (WebFetch allowlist):** openai.com, anthropic.com, techcrunch.com,
artificialintelligenceact.eu, block.xyz. help.openai.com and support.claude.com work.

## Material to ask for once the script is OK

- NEEDED: both help pages above, saved as PDFs from Safari, into `work/pdf/` (git-ignored). They become the
  highlighted crops, as in #9 (`pdfwords.py` and `make_pages.py`).
- OPTIONAL: OpenAI's announcement page (openai.com/index/eu-text-provenance) as a PDF, for a dated headline card.

## Build rules for #10 (Content Hub "Raising the bar")

- Lean build: real pages, my own graphics, at most 2 Flow clips (cap 10) and at most 5 images. No stock footage for
  the creator to download.
- The claim on the first frame, the everyday picture by 0:10, at most two pieces of text on screen, the catch, then a
  practical ending that loops back to the hook. Length 60–85 s, under 90.
- Reuse `library/3d` before fetching anything new (check for a coin; Fluent has one).
- Visual ideas:
  - a coin flipping over word pairs (big/large, start/begin)
  - matching words lighting up until a signature draws itself
  - copy, paste and screenshot icons failing to remove it
  - a map with Paris signed and London "not yet"
  - two detection bars, 69% and 42%
  - your own sentence going through a translator and coming out signed
  - the "not fully conclusive" quote card
  - a teacher's checker padlocked
  - "say so" as the end beat

## Demand signals (vidIQ, 24 Oct)

- Breakout Short "Teachers, are you see this too?!? #ai … #cheating": 472.6k views on a channel with 285 subscribers
  (251× its usual).
- Konkuk University voided a midterm for about 600 students after AI cheating (Seoul Economic Daily, 23 Oct).

## Accounts and posting

- vidIQ: the channel is now connected (One AI Trick, @1aitrick, UCp7iNYgAxKPmnzJqFAjt5HA). 140 of 150 credits left;
  they renew 24 Nov; most calls cost 5.
  - Planned: `vidiq_subscriber_insights` for the posting hour, and `vidiq_score_title` on 2–3 YouTube titles.
  - Skip vidIQ's script, voice, video and music generators.
- Windsor.ai YouTube connector: account 63477, for the scorecard.
- The creator posts #9 (claim title on the first frame) and handles #4 on the morning of 24 Oct. #10 goes up at least
  24 h after #9.
