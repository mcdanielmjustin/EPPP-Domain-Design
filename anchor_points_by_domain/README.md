# EPPP Anchor Points by Domain (v2.13)

## Overview

This folder contains **1,567 anchor points** organized across **9 domains** for EPPP exam preparation. Each anchor point represents a discrete, testable piece of knowledge derived from the PrepJet CSV source and reorganized according to pedagogical design principles.

---

## File Structure

Each domain file follows this format:

```
================================================================================
DOMAIN X: [DOMAIN NAME]
================================================================================
Total Anchor Points: [COUNT]
================================================================================

--------------------------------------------------------------------------------
[CODE]: [Subdomain Name] ([X] items)
--------------------------------------------------------------------------------

[ID] Anchor point content summary...
```

---

## Domain Summary

| Domain | Name | Anchor Points | Type | F/M Ratio |
|--------|------|---------------|------|-----------|
| D1 | Psychometrics & Research Methods | 193 | BIG 4 | 60/40 |
| D2 | Lifespan & Developmental Stages | 174 | BIG 4 | 55/45 |
| D3 | Clinical Psychopathology | 134 | Standard | 30/70 |
| D4 | Psychotherapy Models, Interventions, & Prevention | 168 | Standard | 25/75 |
| D5 | Social & Cultural Psychology | 153 | BIG 4 | 50/50 |
| D6 | Workforce Development & Leadership | 172 | Standard | 30/70 |
| D7 | Biopsychology | 192 | BIG 4 | 45/55 |
| D8 | Clinical Assessment & Interpretation | 190 | Standard | 30/70 |
| D9 | Psychopharmacology & Ethics | 191 | Capstone | 30/70 |
| **TOTAL** | | **1,567** | | |

**F/M Ratio** = Fundamental / Mastery percentage split for adaptive learning

---

## Subdomain Code Reference

Each anchor point is categorized by a **3-letter subdomain code** indicating its original content area:

| Code | Full Name | Description |
|------|-----------|-------------|
| **CLI** | Clinical Psychology | Therapies, interventions, cross-cultural issues |
| **ETH** | Ethics | APA Ethics Code standards, professional issues |
| **LEA** | Learning | Classical/operant conditioning, memory, learning interventions |
| **LIF** | Lifespan Development | Cognitive, physical, socioemotional development |
| **ORG** | Organizational Psychology | I/O psychology, leadership, career development |
| **PAS** | Psychological Assessment | Clinical tests, MMPI, Wechsler, personality measures |
| **PHY** | Physiological Psychology | Brain structures, neurotransmitters, psychopharmacology |
| **PPA** | Psychopathology | DSM disorders, diagnostic criteria, etiology |
| **RMS** | Research Methods & Statistics | Study designs, statistical tests, validity |
| **SOC** | Social Psychology | Social cognition, attitudes, persuasion, group influence |
| **TES** | Tests & Measurement | Reliability, validity, test construction, score interpretation |

---

## Anchor Point ID Numbering System

Each anchor point has a unique identifier in brackets `[ID]` with two formats:

### Format 1: Simple Numeric ID
```
[001], [009], [020], [105], [217]
```
- Original item numbers from the PrepJet CSV source
- Preserves traceability to source material

### Format 2: Compound ID (Hyphenated)
```
[01-1], [02-3], [07-2], [11-3]
```
- First part: Topic/concept cluster number
- Second part: Variant or related item within that cluster
- Used when multiple anchor points address the same core concept from different angles

### ID Characteristics
- IDs are **NOT sequential** within subdomains (preserves original source mapping)
- Bare `[ID]` values are **NOT unique within a domain** — 75 anchor groups share the same `(domain, subdomain_code, anchor_id)` triple with different content (see `anchor_uid_index.json` `_metadata`)
- The **`uid`** field (e.g., `D1-LEA-009-f89cf513`) is the canonical unique identifier — always key on `uid`, not on the bare ID
- A human-readable self-disambiguating form exists: **`anchor_point_id_v2`** — format `AP-D{n}-{SUBCODE}-{anchor_id}` (e.g., `AP-D1-LEA-009`). Mechanically derivable from the uid; used in the authored question CSVs (mock exam, enrichment, fundamentals) alongside the legacy `anchor_point_id` column
- IDs allow **cross-referencing** back to source CSV (`eppp_exam_questions.csv`)

---

## Subdomain Categories by Domain

### Domain 1: Psychometrics & Research Methods
- LEA: Classical Conditioning, Operant Conditioning
- RMS: Variables/Data, Internal/External Validity, Research Designs, Inferential Statistics, Correlation/Regression
- TES: Item Analysis/Reliability, Test Validity (Content, Construct, Criterion-Related), Score Interpretation

### Domain 2: Lifespan & Developmental Stages
- LIF: Cognitive Development, Physical Development, Language Development
- LIF: Socioemotional Development (Attachment, Temperament, Moral Development)
- LIF: Early Influences (Nature vs. Nurture, Prenatal), School and Family Influences

### Domain 3: Clinical Psychopathology
- PPA: Neurodevelopmental Disorders, Schizophrenia Spectrum, Bipolar/Depressive Disorders
- PPA: Anxiety/OCD, Trauma/Stressor-Related, Feeding/Eating/Sleep Disorders
- PPA: Substance-Related, Neurocognitive, Personality Disorders, Sexual Dysfunctions

### Domain 4: Psychotherapy Models, Interventions, & Prevention
- CLI: Cognitive-Behavioral Therapies, Psychodynamic/Humanistic Therapies
- CLI: Family/Group Therapies, Brief Therapies
- CLI: Prevention, Consultation, Psychotherapy Research
- LEA: Interventions Based on Classical/Operant Conditioning

### Domain 5: Social & Cultural Psychology
- SOC: Social Cognition (Attributions, Biases/Heuristics)
- SOC: Attitudes, Persuasion, Social Influence (Group, Types)
- SOC: Affiliation/Attraction, Prosocial Behavior, Prejudice/Discrimination
- CLI: Cross-Cultural Issues (Identity Development, Terms/Concepts)

### Domain 6: Workforce Development & Leadership
- ORG: Job Analysis, Performance Assessment, Employee Selection
- ORG: Training Methods, Organizational Theories, Leadership
- ORG: Motivation, Satisfaction/Commitment/Stress
- ORG: Career Choice/Development, Organizational Change/Development

### Domain 7: Biopsychology
- PHY: Nervous System, Neurons, Neurotransmitters
- PHY: Brain Regions (Cerebral Cortex, Hindbrain/Midbrain/Subcortical)
- PHY: Sensation/Perception, Memory/Sleep, Emotions/Stress
- PHY: Neurological/Endocrine Disorders

### Domain 8: Clinical Assessment & Interpretation
- PAS: Stanford-Binet, Wechsler Tests, Other Cognitive Ability Measures
- PAS: MMPI-2, Other Personality Measures, Clinical Tests, Interest Inventories
- LEA: Memory and Forgetting (assessment-relevant)

### Domain 9: Psychopharmacology & Ethics
- PHY: Psychopharmacology (Antipsychotics, Antidepressants, Other Psychoactive Drugs)
- ETH: APA Ethics Code (Standards 1-10), Professional Issues

---

## Design Principles

This 9-domain structure implements:

1. **Big 4 Dispersal** - Foundational domains at positions 1, 2, 5, 7 for cognitive pacing
2. **Prerequisite Chain** - D7 (Biopsychology) prerequisites D9 (Psychopharmacology)
3. **Bloom's Taxonomy Progression** - Higher Fundamental% in early domains, higher Mastery% in later domains
4. **Balanced Domain Sizing** - All domains constrained to 130-200 anchor points
5. **Thematic Coherence** - Each domain has a distinctive "personality" and thematic lean

---

## Related Files

| File | Description |
|------|-------------|
| `../FINAL_9_DOMAIN_STRUCTURE.md` | Complete structure documentation with rationale |
| `../DOMAIN_DESIGN_CONSTRAINTS.md` | Design rules and constraints |
| `../DOMAIN_SUMMARY_TABLES.txt` | Summary statistics and tables |
| `../eppp_exam_questions.csv` | Original source CSV (1,570 items) |
| `../export_domains.py` | Script used to generate these domain files |
| `../../EPPP_Comprehensive_Domain_Comparison_Report.txt` | Full comparison vs ASPPB and PrepJet |

---

## Version

**Version:** 2.13
**Total Anchor Points:** 1,567
**Generated:** January 2, 2026
**Transformation from PrepJet:** 15.5% (244 points reorganized)
