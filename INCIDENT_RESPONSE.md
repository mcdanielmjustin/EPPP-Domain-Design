# Copyright Incident Response Playbook

What to do if a copyright claim, DMCA notice, cease-and-desist, or threat
of litigation arrives.

**Read this before responding to any contact alleging copyright
infringement.** Not a substitute for legal counsel — this is an
operational runbook.

---

## First-response discipline (within 1 hour of contact)

1. **DO NOT reply with substance.** Acknowledge receipt, state you are
   reviewing, and commit to a response within 14 business days (DMCA
   standard). Template:

   > Thank you for your message. We take copyright matters seriously and
   > are reviewing the details you provided. We will respond
   > substantively within 14 business days.

2. **DO NOT admit infringement, derivation, or any shared source.** Even
   a casual "we might have some overlap" can weaken a defense.

3. **DO NOT delete, rewrite, or quietly modify the accused content.**
   Evidence-preservation discipline matters. The `_b4_findings.md`,
   `_explanation_overlap_report.json`, backup chains, session logs, and
   PROVENANCE.md are all evidentiary. Do not silently scrub them.

4. **FREEZE merges on the repo.** Post a pin in team chat:
   > Content merges paused pending legal review. Do not merge copyright-
   > related rewrites or cleanups.

5. **Capture the inbound message** (email headers, sender details, any
   attached exhibits). Save to `_incident_YYYY-MM-DD/`.

---

## Classify the claim type

| Contact type | Typical form | Timeline |
|---|---|---|
| **DMCA takedown** | Notice filed via copyright agent, alleging specific infringing URLs/content | Hosting/CDN (Vercel) processes takedown in hours if form is valid; we have 10–14 days to file counter-notice |
| **Cease-and-desist** | Letter from opposing counsel, usually demanding removal + damages; may reference specific content | Response window 14–30 days typically |
| **Lawsuit** | Complaint filed in federal court (copyright is federal jurisdiction) | Answer due within 21 days of service |
| **Informal** | Email from competitor's founder or legal contact, less formal | Treat seriously; same evidence discipline |

---

## DMCA takedown response flow

1. **Verify the notice is valid** (see 17 U.S.C. § 512(c)(3)):
   - Physical or electronic signature of authorized person
   - Identification of the copyrighted work
   - Identification of the allegedly-infringing material with enough
     specificity to locate (URL, file, or content snippet)
   - Contact information for the complainant
   - Statement that complainant has good-faith belief in infringement
   - Statement under penalty of perjury that the notice is accurate and
     authorized

   **If any element is missing**: the notice is defective and may be
   returned without action. Consult counsel before rejecting, though.

2. **Take down the specific content** if the notice is valid:
   - Identify the specific UIDs / row IDs named
   - For questions: set `option_a-d`, `correct_answer`, `explanation`
     to empty string in Supabase (targeted SQL UPDATE) — do NOT delete
     the rows (need them for counter-notice audit)
   - For anchor_points: set `text` to empty string for targeted UIDs
   - Regenerate the website bundle excluding those UIDs; push; Vercel
     rollback chain is the emergency undo

3. **Preserve the removed content** in `_removed_under_dmca_YYYY-MM-DD/`
   (offline, non-shipped, evidentiary).

4. **Notify complainant** that material has been removed.

5. **Decide: counter-notify or not.** If we believe the claim is wrong
   (e.g., the content is facts not expression, or is our own independent
   rewrite), file counter-notice within 10–14 business days citing
   PROVENANCE.md and the rewrite-commit chain. Counter-notice restores
   content after 10–14 days unless complainant sues.

---

## Emergency content takedown — the one-click paths

**Website bundle rollback** (restores prior safe Vercel deploy):
- Go to Vercel dashboard → PassEPPP-website project → Deployments
- Find the last known-safe deployment (pre-incident)
- Click "…" → "Promote to Production"
- Takes ~30 seconds. Live site reverts.

**Supabase content redaction** (for specific UIDs):
```sql
UPDATE anchor_points
SET text = ''
WHERE uid IN ('D1-SUB-009-...', 'D2-SUB-014-...');

UPDATE questions
SET option_a = '', option_b = '', option_c = '', option_d = '',
    correct_answer = '', explanation = ''
WHERE id IN (...);
```
Keep the rows. Keep the originals in local backups
(`backup_cascade_20260418_183547`, etc.). Do NOT `DELETE FROM` anything.

**Local CSV redaction** (for remediation before next push):
- Edit the row in place, keep the backup chain intact
- Commit with message `Redact UIDs per incident <ID>` — do not reference
  the specific claim text in the commit message

---

## Retain counsel — who to call

**IF NOT ALREADY ENGAGED**: identify a psychology-ed-tech IP attorney in
advance, not at the moment of crisis. Suggested profile:
- Federal litigation experience (copyright is federal jurisdiction)
- Software / content-platform copyright experience
- Comfortable with AI-assisted content provenance questions

**When to call**:
- Any formal legal document (C&D, complaint)
- Any DMCA notice where we want to counter-notify
- Any communication suggesting litigation is planned
- Before filing the DMCA designated-agent registration is also a good
  time to have a 30-minute consult

Budget: expect $400–700/hr for IP counsel. Maintain a $5–10K retainer
for incident response.

---

## Evidence package to have ready on day 1

When counsel is retained, send:
1. `PROVENANCE.md` (this folder)
2. `STYLE_GUIDE.md` (this folder)
3. Rewrite-commit hashes: `3c6dae5`, `1108766`, + newer cleanup commits
4. `_b4_findings.md` + `_explanation_overlap_report.json` (audit outputs)
5. Backup chain listing (directory listing of `backup_cascade_*` files)
6. Session logs: `eppp-claude-context/session_changes_2026-04-1{8,9}.txt`
7. The third-party reference CSV (as EXHIBIT for comparison, not as our
   content) with explanation: "kept for audit only, never shipped, never
   committed"

---

## Defensive positioning (factual, not legal advice)

Our content is defensible because:

- **Facts are not copyrightable** (*Feist*, 1991). Our anchor summaries
  test the same facts as the EPPP Candidate Handbook and named
  textbooks — facts to which no one holds a monopoly.
- **Expression is rewritten.** The 2026-04-18/19 remediation replaced
  99.2% → 0% of verbatim-matching anchor content with primary-source-
  cited paraphrases. Deep-audit at 98.7% clean. Commits `3c6dae5`,
  `1108766`.
- **Structure is independent.** 9 domains vs 8 in the Handbook; 121
  chapter titles vs ~109 in any competitor reference, zero title overlap.
- **Distractor metadata is proprietary.** Bloom's-tagging,
  misconception-categorization, and adaptive-flashcard spawn logic are
  our own product design, not inherited from any source.
- **Identifier scheme is independent.** Our canonical UID is a
  content-addressed hash, derived from (domain, subdomain, bare,
  verbatim_text) via our own algorithm.

---

## What NOT to do under any circumstance

- Do not reply to a C&D letter or DMCA notice without counsel reviewing
  the draft.
- Do not admit on the record that any content is "derived from" or
  "inspired by" or "based on" the third-party source.
- Do not hastily delete Git history or squash commits — the rewrite
  commits ARE the evidence of remediation.
- Do not delete session logs, backup files, or audit reports. If a
  claim is frivolous, these show due diligence; if valid, they show
  remediation in good faith.
- Do not negotiate settlement without counsel.
- Do not post public statements (blog, Twitter, support forum) about the
  incident while it is active.

---

## After the incident — post-mortem items

Once resolved:
1. Update PROVENANCE.md with the incident's resolution date + outcome
2. Add any new precedent (e.g., "explanation-vs-explanation overlap
   threshold lowered to 30%") to STYLE_GUIDE.md
3. Update Tier E sentinel rules if new patterns emerged
4. Refresh the incident-retainer amount if spent
5. File away the evidence package as `_incident_<date>_resolved/`

Last updated: **2026-04-19**.
