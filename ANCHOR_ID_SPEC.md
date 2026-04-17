# EPPP Anchor Identifier Specification

**Version:** 1.0 (2026-04-16)
**Status:** Canonical. When any file or script is ambiguous about identifier usage, this document wins.

---

## 1. The four identifier forms

Each anchor point has up to four identifiers in active use. They are **not interchangeable**.

| # | Form | Example | Properties |
|---|---|---|---|
| 1 | **Bare ID** | `[009]` or `009` | Section-scoped. **NOT unique** within a domain. Inherited from the PrepJet source CSV. Preserved for traceability only. |
| 2 | **UID** (canonical) | `D1-LEA-009-f89cf513` | **Globally unique.** Carries domain + subdomain + bare ID + 8-char hex disambiguator. The authoritative primary key. |
| 3 | **Legacy AP** | `AP-D1-009` | Domain-scoped, **NOT unique** within a domain (same collision as bare ID). Used in historical CSV exports and deployed JSON artifacts. Kept for backward compatibility — do not change existing values. |
| 4 | **v2 AP** (recommended) | `AP-D1-LEA-009` | Self-disambiguating human-readable form. Unique except for 75 within-subdomain collision groups where the disambiguator is still needed (see §5). Mechanically derivable from the UID. |

---

## 2. Canonical precedence

When multiple IDs are present on a record, prefer in this order:

**uid → anchor_point_id_v2 → anchor_point_id (legacy AP) → bare anchor_id**

Treat the `uid` as the real primary key. Treat `v2` as the display/collation form. Treat the legacy forms as read-only legacy that you must preserve but should not write new code against.

---

## 3. v2 derivation

```
v2 = f"AP-D{domain_num}-{subdomain_code}-{anchor_id}"
```

Three equivalent sources for the components, in preference order:

1. **From UID** (preferred): parse `D(\d+)-([A-Z]{3})-(.+)-[0-9a-f]{8}$` → `(domain_num, subdomain_code, anchor_id)`
2. **From triple of columns**: `(domain_id, source_code, original_id)` when stored (e.g., `JustinQuestionsDatabase-2.0/data/reference/anchor_points.json`)
3. **From CSV triple**: `(domain_code→domain_num, anchor_subdomain_code, anchor_point_id)` when stored (e.g., enrichment CSV)

Note: `v2` is **not** guaranteed unique — 75 groups have identical `(domain_num, subdomain_code, anchor_id)` but different content (see §5). In those groups, use the UID hex disambiguator.

---

## 4. File-to-format matrix

### Source-of-truth files (authored)

| File | Identifier fields present |
|---|---|
| `Downloads/ANCHOR POINTS SORTED/Domain_*.txt` | bare `[ID]` only |
| `Downloads/ANCHOR POINTS SORTED/anchor_uid_index.json` | bare, uid, domain_num, subdomain_code, in_book flag |
| `EPPP-Domain-Design/anchor_points_by_domain/Domain_*.txt` | bare `[ID]` only (content-identical to Downloads) |
| `EPPP-Domain-Design/anchor_points_by_domain/anchor_uid_index.json` | same as Downloads variant |
| `EPPP-Domain-Design/eppp_exam_questions.csv` | PrepJet-format bare |
| `Desktop/chapter_schema_v3.xlsx` | anchor_id (bare), **anchor_id_v2**, uid, verbatim_anchor |
| `JustinQuestionsDatabase-2.0/data/reference/anchor_points.json` | id (legacy AP), original_id (bare), source_code, domain_id, **id_v2** |

### Authored question datasets

| File | Identifier fields present |
|---|---|
| `Desktop/mock_exam_questions.csv` + `.xlsx` | anchor_point_id (legacy AP), **anchor_point_id_v2**, anchor_uid |
| `Desktop/2026/enrichment_all_questions.csv` | anchor_point_uid, anchor_point_id (bare), **anchor_point_id_v2**, anchor_subdomain_code, original_anchor_point_ids |
| `Desktop/fundamentals_sorted_master.csv` + `.xlsx` | anchor_point_id (legacy AP), **anchor_point_id_v2** |

### Deployed / production artifacts (read-only by this spec)

| File | Identifier fields present | Notes |
|---|---|---|
| `PassEPPP-website/content/enrichment/{DOMAIN}_quiz.json` | anchor_point_ids (array of legacy AP), sometimes anchor_uid | No v2 yet; deferred |
| `PassEPPP-website/content/mock_exams_v2/exam_*.json` | anchor_point_ids (array of legacy AP) | No v2 yet; deferred |
| `JustinQuestionsDatabase-2.0/data/mock_exams/exam_*.json` | anchor_point_ids (array of legacy AP) | No v2 yet; deferred |
| Supabase `question_bank.anchor_point_ids TEXT[]` | legacy AP | No v2 column; deferred |
| Supabase `flashcard_progress.anchor_point_ids TEXT[]` | legacy AP | No v2 column; deferred |
| `PassEPPP-website` localStorage state | legacy AP embedded in question objects | Any schema change must invalidate cache |

### Mastery modules (not affected)

`JustinMasteryPage/data/*.json` (spot, tables, vignettes, passages) use module-specific fully-qualified IDs (`BPSY-0338`, `BPSY-TBL-0001`, `JQ-LEA-136-vignette-L1`). They do **not** key on the anchor identifier system at all.

---

## 5. Collision facts

All counts from `anchor_uid_index.json` `_metadata` (canonical source).

- **Total anchors:** 1,567 (1,081 in-book + 486 proprietary)
- **Within-subdomain ID groups with duplicate content:** 75. Same `(domain_num, subdomain_code, anchor_id)` triple, different `verbatim_anchor`. The UID hex suffix disambiguates.
- **True content duplicates:** 4 — same `verbatim_anchor` under different anchor IDs. These are genuine source-level duplicates.

| Content-duplicate UIDs | Notes |
|---|---|
| D3-PPA-02-2 | paired |
| D4-CLI-183 | paired |
| D6-ORG-003 | paired |
| D8-PPA-18 | paired |

- **Cross-section ID reuse within a domain:** 431 unique bare IDs across 1,567 entries. A bare ID like `[009]` can appear in up to 3 different subdomain sections within the same domain.

---

## 6. Known gaps (2026-04-16 snapshot)

These are documented but intentionally unresolved pending content-matching work:

- **Enrichment CSV**: 1,700 / 12,726 rows have no `anchor_point_uid` and no `anchor_subdomain_code` — `anchor_point_id_v2` left blank. Source questions lack enough metadata to derive v2.
- **Fundamentals CSV**: 765 / 3,381 rows have a legacy AP ID that matches multiple `(domain, subdomain, bare_id)` triples — v2 cannot be derived without reading question content. Listed in `fundamentals_v2_ambiguous.json`.
- **Fundamentals CSV**: 81 / 3,381 rows have a legacy AP ID that matches zero entries in `anchor_uid_index.json` — anchor not in the index.
- **Chapter schema**: 2 UIDs present in schema are NOT in `anchor_uid_index.json` (`D3-PPA-02-1-298ce60f`, `D6-ORG-14-1-9b33e6f6`). Schema or index is out of sync.
- **Mock exam**: 2 UIDs (`D8-PAS-120-bcc355b2`, `D6-ORG-25-3-5aa946f1`) are in the index but not in the chapter schema. Schema is missing these 2 book anchors.

These gaps are tracked, not blocking. Closing them is content-dependent and out of scope for identifier standardization.

---

## 7. Rules for new code

1. **Primary key is `uid`.** If you're writing new storage, join, or lookup logic, use `uid`.
2. **Don't rename the legacy fields.** `anchor_point_id` stays as-is in every CSV, JSON, and DB column. `v2` is additive.
3. **v2 is derived, not authored.** If you have uid or (domain_num + subdomain_code + anchor_id), you can always recompute v2. It is not manually maintained.
4. **Deployed JSONs and Supabase are frozen at legacy format** until a formal migration plan authorizes v2 propagation.
5. **When you see a bare `[009]` or `AP-D1-009` and it's ambiguous, that's expected.** Always disambiguate via UID or v2 before acting.

---

## 8. Change log

- **2026-04-16** (v1.0): Initial spec. Added `anchor_point_id_v2` to mock exam CSV, enrichment CSV, fundamentals CSV. Added `anchor_id_v2` column to `chapter_schema_v3.xlsx`. Added `id_v2` field to `JustinQuestionsDatabase-2.0/data/reference/anchor_points.json`.

---

## 9. Related files

- `anchor_points_by_domain/README.md` — per-domain txt file format
- `anchor_points_by_domain/anchor_uid_index.json` — canonical disambiguator
- `DOMAIN_DESIGN_CONSTRAINTS.md` — upstream design rules
- `FINAL_9_DOMAIN_STRUCTURE.md` — domain structure rationale
