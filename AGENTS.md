# Blueprint for agents working on this profile

Read this first, then `tools/README.md` for the mechanics. This file is the why and the how-to-decide; that one is the how-to-build.

## What this is

`README.md` renders on github.com/DryMertini. It is only `<picture>` tags pointing at generated SVGs in `art/`. Each project repo that gets the treatment has one matching animated header at the top of its own README. Never hand-edit an SVG: change the scripts in `tools/` and regenerate.

## The look

- **Blueprint, not neon.** Thin outlines, construction lines left visible, wireframe depth. No glows on text, no gradient-filled lettering, no shiny sweeps. Glow is allowed only on small moving things (pulses, a status dot).
- **Depth by default.** Everything gets a back face offset down-right with corner links (`letters.word(depth=…)`, the `frame()` helper, card slabs). If you add an element and it is flat, it is unfinished.
- **Palette** lives in `PAL` in `tools/gen.py`, dark and light. Muted gold for lines (`nm`), light ink for neutral lines, green only for "working / passed / charged", burnt orange only for slab edges. Don't add colours.
- **Type.** Names and repo titles use the constructed lettering in `letters.py`. Everything else is plain system sans or mono, flat. One short line of description, one mono line of tags.
- **Motion says something.** Fast, parallel, looping; nothing that makes work look slow. Each animation should show what the thing does (stacks swapping, a maze being solved, layers passing checks). No decoration that could sit on any repo.
- **Short.** No badges, no stats widgets, no emoji, no adjectives about the owner. Facts and artefacts carry it.

## Adding a new repo

1. **Read it before drawing.** README, entry point, tests, any results table. Write down in one sentence what it actually does and the one mechanism that makes it interesting.
2. **Pick the metaphor from the contents**, in this order: the repo's own name if it is a real object (plumbline → a plumb bob); else its core data structure or algorithm in motion; else its pipeline stages lighting in order. If two candidates fit, take the one a stranger would decode in three seconds.
3. **Only real numbers.** A figure goes on a card only if it is in the repo's own README or reports. Quote it exactly; don't round up, don't invent.
4. **Repo header** (`tools/proj.py`): framed 838×196, title in blueprint letters at scale 0.5, subtitle, tags, artwork on the right from x≈500. Add any missing glyphs to `GLYPHS` first.
5. **Profile card** (`tools/gen.py`): solo work gets a full-width card, team/hackathon work a half-width one. Label says which (`SOLO BUILD`, `HACKATHON BUILD`). Reuse the header's artwork function so both match.
6. **Touch the repo's README as little as it needs.** If it is already good, swap only the title for the header. If it is cluttered, cut to: what it does, how it works in three bullets, numbers, how to run.
7. Regenerate, copy scripts into `tools/`, update the table in `tools/README.md`.

## Checks before merging

- `xmllint --noout` on every SVG.
- Every non-discrete SMIL animation: `keyTimes` starts at 0, ends at 1, never decreases, same count as `values`. A list that stops short is silently dropped by browsers (this hid a whole animation once).
- Render stills with `rsvg-convert` for layout. Stills ignore animation: elements that start at opacity 0 or are moved by `animateMotion` won't show or will sit at 0,0. Check motion on the live page.
- Look at both themes. Text must stay readable on white.
- GitHub caches images about five minutes; same filename means wait, a query string does not bust it.

## Shipping

- One pull request per change, merged into the default branch. Small and named for what changed.
- Show the owner a still before anything that changes the look; fixes and additions he already asked for can go straight in.
- Nothing goes on the page that the owner cannot back up if asked about it in an interview.
