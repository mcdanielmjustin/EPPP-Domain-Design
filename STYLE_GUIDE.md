# Content Authoring Style Guide

Required reading for every contributor authoring EPPP content (anchor
summaries, question stems, distractor options, explanations, flashcard
seeds, vignettes).

---

## Three rules that take priority over everything else

1. **Never copy-paste from the third-party reference CSV** (`eppp_exam_questions_prepjet.csv`). The file exists only at
   `C:\Users\Admin\eppp-claude-context\textbook\` for audit reference.
   Never open it in a tab while authoring new content, never pipe it into
   an AI prompt, never use it as "inspiration." If you need to learn what
   the exam tests, read the EPPP Candidate Handbook (ASPPB) or a named
   textbook.

2. **Cite a primary source for every factual claim.** Our anchor-rewrite
   format is: `Author (Year): <paraphrased fact>` — e.g.
   `Linehan (1993): DBT individual therapy targets life-threatening,
   therapy-interfering, and quality-of-life interfering behaviors in that
   priority order.` When no named primary source exists, use a descriptive
   opener: `In standard practice,` / `Clinical research indicates that,` /
   `Current guidelines recommend that,`.

3. **Never modify the HARD-LOCKED columns** in any question CSV without
   explicit sign-off. These drive adaptive flashcards, the Bloom's-tagged
   achievement-gap algorithm, and user-progress analytics — they are our
   product moat.

   | Column                           | CSV              |
   |----------------------------------|------------------|
   | `option_a` / `_b` / `_c` / `_d`  | all 3            |
   | `correct_answer`                 | all 3            |
   | `explanation` / `explanation_a-d`| mock, fund / enr |
   | `tested_concept[_id/_label]`    | mock, enr        |
   | `knowledge_tested`               | enr              |
   | `flashcard_*_front` / `_back`    | enr              |
   | `distractor_1-3_letter/level/misconception_type` | enr |
   | `blooms_primary` / `_secondary`  | enr              |

---

## Voice and phrasing

### Preferred sentence openers for paraphrased facts

- `<Author> (<Year>) found / proposed / demonstrated that …`
- `In <Author>'s <Year> <study type>, …`
- `Clinical research indicates that …`
- `Current guidelines recommend …`
- `Standard practice holds that …`

### Patterns to avoid

- **Sentence openings that mirror the third-party CSV.** Variety matters.
  Do not start 10 consecutive anchor summaries with "The goodness-of-fit
  model …" the way a source does.
- **Verbatim enumerations of >5 items** from a single named list. Reorder,
  regroup, or summarize.
- **Quoted-looking phrasing** like "stands as one of the most influential
  models" — this reads like ad copy and often is verbatim-ish.
- **"Based on" framing** ("This question is based on the work of …") —
  just cite the primary source directly.

---

## Factual fidelity is non-negotiable

Facts not copyrightable (*Feist v. Rural Telephone*, 1991), but facts
must be preserved exactly across paraphrase. Specifically:

- **Numbers** — time windows, dosages, percentages, effect sizes
- **Technical terms of art** — "dialectical behavior therapy," "NEO-PI-3,"
  "T-score," "goodness-of-fit model" — keep verbatim
- **Named researchers** — "Linehan," "Cattell," "Kohlberg," "APA," "DSM-5-TR"
- **Study years** — 1927, 1993, 1983, etc.
- **Clinical criteria** — DSM / ICD diagnostic thresholds must match the
  current edition exactly

If paraphrase forces you to drop a testable fact, you are paraphrasing
too aggressively. Restart with the structural rearrangement approach,
not the content-reduction approach.

---

## Authoring workflow for new anchors

1. **Source**: read the primary source (Handbook section, named textbook
   chapter, named journal article). Do NOT consult the third-party source CSV.
2. **Draft anchor_content_summary**: 1–3 sentences, in our voice, citing
   the primary author where one exists.
3. **Assign identifier**: generate a UID via the canonical
   `D{n}-{SUB}-{bare}-{hex8}` format. The hex is a deterministic hash of
   (domain, subdomain, bare, verbatim_text) — our script handles this.
4. **Run the sentinel**: `python scripts/copyright_sentinel.py --check <uid>`
   (Tier E1) — the draft must show <40% 5-gram overlap with any row in
   the third-party reference corpus before it can be committed.
5. **Commit**: with a message documenting the primary source consulted.

## Authoring workflow for new questions

1. **Pick the anchor** you are testing (canonical UID).
2. **Read the anchor_content_summary** (our paraphrased text) and the
   primary source it cites.
3. **Write the stem and the correct answer first**, then author 3
   distractors tied to specific misconception-type categories
   (`misconception_type` column values). Each distractor should be
   traceable to a real pedagogical error, not random wrong-sounding text.
4. **Write the multi-option explanation** (or 4 split explanations for
   enrichment). Explanations must reference the anchor summary and the
   primary source; do NOT copy from the third-party CSV's rationale
   column.
5. **Tag `blooms_primary` / `blooms_secondary`** based on the cognitive
   demand of the stem (Remember/Understand/Apply/Analyze/Evaluate/Create).
6. **Tag `tested_concept`** — the specific concept the correct answer
   pivots on.
7. **Run the sentinel + run the distractor-immutability check** before
   committing.

---

## What to do if you suspect an existing row has copyright risk

1. **Do not edit the HARD-LOCKED columns.** If the issue is in
   `option_a-d`, `correct_answer`, `explanation`, or
   `tested_concept`/`misconception_*`/`blooms_*`/`distractor_level`:
   document in `_copyright_review_queue.md` and flag the row for the
   scope owner. Do not auto-rewrite.
2. If the issue is in `anchor_content_summary` or any other shippable
   narrative field, run the paraphrase pipeline in
   `scripts/rewrite_uncovered_91.py` on the specific UID(s) and commit
   with a message referencing this style guide.
3. If in doubt, ask. An unfixed known risk is better than a broken
   algorithm.

---

## What NEVER belongs in a shipped artifact

- The literal substring `PrepJet` (any capitalization)
- The substring `EPPP-P1-` through `EPPP-P7-`
- The substring `EPPP-F1-` through `EPPP-F9-`
- The substring `-PPY-` (legacy subdomain-code typo, resolved)
- The column name `anchor_content_summary_original` (audit-only)
- Any field named `source_exam`, `source_question_id`, or
  `source_question_number` (third-party provenance breadcrumbs)
- Full PrepJet-style chapter titles as visible text

Tier E2's pre-commit hook will block commits introducing these substrings
under `content/` paths.

---

## When this guide itself must be updated

After any of:
- New source being approved for paraphrase authority
- New HARD-LOCKED column being added (mirror in the table above and in
  `verify_distractors_unchanged.py`)
- New blocked substring being added to Tier E2's pre-commit hook
- Resolution of a copyright-review queue item that establishes a
  new-precedent phrasing pattern worth codifying

Last updated: **2026-04-19**.
