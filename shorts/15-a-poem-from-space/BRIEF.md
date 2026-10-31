# Short #15: "Google sent an AI to space. Its first words were a poem" (brief and handoff)

Numbered #15: #14 ("Four AIs got out") is being made in another session. Hub tab: "#15 A poem from space" (order b15).

Status on 30 Oct 2026: the creator picked this pitch (2 of 3). `script.txt` is draft v2, **waiting for the creator's
OK** before they record it in ElevenLabs (their own cloned voice). Nothing is built yet.

**v2 (30 Oct):** the creator wants a longer, explained short (Shorts run up to 3 minutes) with every second kept
interesting. About 500 spoken words, roughly 2:48 at #13's pace. v1 (245 words, ~82 s) is in git history.

The other two pitches, not picked: "It asked for help through the phone book" (OpenAI's agent that reached an outside
chatbot through DNS, OpenAI misalignment report 25 Sep 2026; offline-training policy 23 Oct) and "Switch the AI off,
and doctors got worse" (Budzyń et al., Lancet Gastroenterology & Hepatology, Aug 2025: 28.4% → 22.4%).

## The story

Hook → evidence → twist → takeaway. Google's Project Suncatcher test satellite (built with Planet, launched 1 Oct 2026
on SpaceX Transporter-18) ran Gemma 4 on a Google TPU in orbit. Its first answer, its "Hello World", was a haiku about
being in space, received as it passed Svalbard. Why space: AI needs ever more electricity, and in a dawn–dusk orbit a
solar panel gets near-constant sun, up to 8× a panel on Earth. Twist: no air in space, so heat only leaves through
radiators; this test runs in short bursts. Catch: one small test; a data center would need clusters of satellites
linked by laser (next two in 2027), and the project lead says it won't be cheaper for years. Takeaway: every AI answer
costs power, and the search for more has left the planet.

**Hidden word: SVALBARD**, on the map pin where the poem came down (line 7). The voice says "the top of the world".

## Facts (checked; primary first; line numbers are script.txt v2)

| Line | Fact | Source |
| --- | --- | --- |
| 1–2, 7 | First AI response from a data-center-class TPU in orbit: a haiku about being in space, asked for by the team; Gemma 4; downlinked as it passed Svalbard | Google, "We've received our first response from the Project Suncatcher prototype satellite", 30 Oct 2026 |
| 4 | Launched 1 Oct 2026 on SpaceX Transporter-18, co-developed with Planet; refrigerator-sized | Google, "Behind Project Suncatcher…", 24 Sep 2026; NPR, 2 Oct 2026 (size) |
| 5 | A data-center-class TPU running Gemma 4 | Google, 30 Oct 2026 |
| 6 | About 90–95 min per orbit at a few hundred km (low Earth orbit physics); uplinks during ground-station passes | Physics; Google, 30 Oct 2026 (ground-station pass) |
| 10 | Data-center electricity use more than doubles by 2030 to about 945 TWh, slightly more than Japan uses today | IEA, Energy and AI, 10 Apr 2025, as quoted by Malay Mail, Invezz, Japan Times. **iea.org won't load from the workspace: confirm on the IEA page before recording, or drop the line** |
| 11 | The Sun emits more than 100 trillion times humanity's total electricity production | Google Research blog, 4 Nov 2025 |
| 13–14 | Dawn–dusk sun-synchronous orbit: near-constant sunlight; a panel up to 8× as productive as on Earth | Google Research, 4 Nov 2025; Google, 24 Sep 2026 |
| 17–19 | No airflow in a vacuum, so heat leaves only through radiators (heat pipes + radiators); thermos and fire are physics analogies | Google, 24 Sep 2026; NPR (no air or water) |
| 20 | Runs in bursts: 15 min at a time for heat (NPR); about 20 min for power (TechCrunch). Voice says "short bursts", no number | NPR, 2 Oct 2026; TechCrunch, 30 Oct 2026 |
| 21–22 | Radiation bit flips; TPUs tested in a proton beam at UC Davis while running AI; survived more than a five-year mission's dose (HBM glitches only at ~3× the expected 5-year dose) | Google, 24 Sep 2026; Google Research, 4 Nov 2025; TechCrunch (bit flips) |
| 23 | Illustrative cluster of 81 satellites, 100–200 m apart, optical (laser) links | Google Research, 4 Nov 2025 |
| 24 | Laser aiming compared to hitting a coin-size target from miles away while both move; twin linked satellites in 2027 | Google, 24 Sep 2026; Google, 30 Oct 2026 |
| 25 | Launch prices may need to fall below $200/kg (mid-2030s); repairs in orbit are hard; Travis Beals doubts it will be cheaper within five years | Google Research, 4 Nov 2025; NPR, 2 Oct 2026 |

Not said on purpose: "first AI in space" (Starcloud flew an Nvidia H100 in Nov 2025); the number of TPUs aboard
(NPR says four, TechCrunch one); the prototype's own orbit (NPR's correction: standard orbit, uses batteries; the
8× line is about "the right orbit").

The haiku is described, not quoted, in the script and captions. Showing Google's own page as proof is a material
decision for the scene sheet.
