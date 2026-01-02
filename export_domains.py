import csv
import os

# v2.3/v2.9/v2.12: Anchor-point-level overrides (highest priority)
# Format: (source, subdomain, anchor_id) -> domain
anchor_point_overrides = {
    # Pharmacology content moved from D3 to D9
    ('PPA', 'Neurodevelopmental Disorders', '03'): 9,  # Antipsychotics for tics
    # Note: ID '21' removed - using content match instead (see pharmacology_keywords)
    ('PPA', 'Bipolar and Depressive Disorders', '27'): 9,  # St. John's wort + SSRI
    ('PPA', 'Bipolar and Depressive Disorders', '157'): 9,  # St. John's wort comparison
    # v2.12: Treatment content moved from D3 to D9
    ('PPY', 'Neurodevelopmental Disorders', '14'): 9,  # Stimulant medication effects on ADHD/SUD
}

# v2.9: Content-based overrides for pharmacology items with duplicate IDs
# Drug-related terms that indicate pharmacology content
drug_terms = [
    'serotonin', 'antipsychotic', 'antidepressant', 'ssri', 'maoi',
    'st. john', 'paroxetine', 'lithium', 'neuroleptic', 'dopamine antagonist',
    'risperidone', 'clozapine', 'haloperidol', 'benzodiazepine',
    'methylphenidate', 'amphetamine', 'anxiolytic', 'mood stabilizer',
]

# v2.11: Option D - Treatment content migration from D3
# Biological/pharmacological treatment keywords -> D9
biological_treatment_keywords = [
    'electroconvulsive therapy', 'ect is', 'ect has', 'ect for',
    'rtms', 'transcranial magnetic',
    'esketamine', 'ketamine treatment', 'sodium oxybate',
    'medication most useful', 'pharmacological treatment',
    'medication are each effective', 'counseling and medication',
]

# Psychosocial treatment keywords -> D8
psychosocial_treatment_keywords = [
    'exposure with response prevention', 'exposure and response prevention',
    'interoceptive exposure', 'in vivo exposure', 'applied tension',
    'cognitive behavior therapy', 'cognitive-behavioral therapy',
    'interpersonal psychotherapy',
    'dialectical behavior therapy', 'dbt ',
    'family-based treatment', 'family-focused therapy',
    'parent-child interaction therapy', 'pcit',
    'multisystemic therapy', 'parent-training', 'ptbm',
    'trauma-focused', 'tf-cbt',
    'community reinforcement', 'motivational interviewing',
    'relapse prevention', 'personalized normative feedback',
    'voucher-based reinforcement', 'vbrt', 'project match',
    'moisture alarm', 'night alarm', 'bell-and-pad',
    'squeeze technique', 'start/stop technique',
    'directed masturbation', 'orgasmic reconditioning',
    'regulated breathing', 'lovaas', 'discrimination training',
    'psychological debriefing', 'videoconferencing therapy',
    'sensate focus', 'kegel', 'vaginal dilators',
]

def is_pharmacology_content(anchor_text):
    """Check if anchor point contains pharmacology-related content."""
    text_lower = anchor_text.lower()
    # Must contain a drug-related term (not just a condition)
    for term in drug_terms:
        if term in text_lower:
            return True
    return False

def is_biological_treatment(anchor_text):
    """Check if anchor point describes biological/pharmacological treatment -> D9."""
    text_lower = anchor_text.lower()
    for term in biological_treatment_keywords:
        if term in text_lower:
            return True
    return False

def is_psychosocial_treatment(anchor_text):
    """Check if anchor point describes psychosocial treatment -> D8."""
    text_lower = anchor_text.lower()
    for term in psychosocial_treatment_keywords:
        if term in text_lower:
            return True
    return False

# Define subdomain to domain mapping based on v2.1 structure
subdomain_mapping = {
    # Domain 1: Psychometrics & Scientific Foundations
    'RMS': 1,  # All RMS goes to Domain 1

    # Domain 6: Organizational Psychology
    'ORG': 6,  # All ORG goes to Domain 6

    # Domain 5: Social & Cultural Psychology
    'SOC': 5,  # All SOC goes to Domain 5
}

# More specific subdomain mappings
specific_mappings = {
    # TES - mostly Domain 1, some Domain 8
    ('TES', 'Item Analysis and Test Reliability'): 1,
    ('TES', 'Test Score Interpretation'): 8,  # v2.2: Moved to D8 (interpretation belongs with assessment)
    ('TES', 'Test Validity - Content and Construct Validity'): 1,
    ('TES', 'Test Validity - Criterion-Related Validity'): 1,

    # PAS - mostly Domain 8, some Domain 1 and 7
    ('PAS', 'Stanford-Binet and Wechsler Tests'): 8,
    ('PAS', 'Other Measures of Cognitive Ability'): 8,
    ('PAS', 'MMPI-2'): 8,
    ('PAS', 'Other Measures of Personality'): 8,
    ('PAS', 'Clinical Tests'): 8,
    ('PAS', 'Interest Inventories'): 8,

    # PHY mappings
    ('PHY', 'Brain Regions/Functions - Cerebral Cortex'): 7,
    ('PHY', 'Brain Regions/Functions - Hindbrain, Midbrain, and Subcortical Forebrain Structures'): 7,
    ('PHY', 'Nervous System, Neurons, and Neurotransmitters'): 7,
    ('PHY', 'Sensation and Perception'): 7,
    ('PHY', 'Memory and Sleep'): 7,
    ('PHY', 'Emotions and Stress'): 7,
    ('PHY', 'Neurological and Endocrine Disorders'): 7,
    ('PHY', 'Neurological and Endocrine disorders'): 7,
    ('PHY', 'Psychopharmacology - Antipsychotics and Antidepressants'): 9,
    ('PHY', 'Psychopharmacology - Other Psychoactive Drugs'): 9,
    ('PHY', 'Psychopharmacology: Antipsychotics and Antidepressants'): 9,

    # LIF - mostly Domain 2
    ('LIF', 'Cognitive Development'): 2,
    ('LIF', 'Physical Development'): 2,
    ('LIF', 'Language Development'): 2,
    ('LIF', 'Socioemotional Development - Attachment, Emotions, and Social Relationships'): 2,
    ('LIF', 'Socioemotional Development - Temperament and Personality'): 2,
    ('LIF', 'Socioemotional Development: Temperament and Personality'): 2,
    ('LIF', 'Socioemotional Development - Moral Development'): 2,
    ('LIF', 'Early Influences - Nature vs. Nurture, Prenatal'): 2,
    ('LIF', 'Early Influences on Development - Nature vs. Nurture'): 2,
    ('LIF', 'Early Influences on Development: Nature vs. Nurture'): 2,
    ('LIF', 'Early Influences on Development - Prenatal Development'): 2,
    ('LIF', 'School and Family Influences'): 2,

    # PPA - mostly Domain 3
    ('PPA', 'Neurodevelopmental Disorders'): 3,
    ('PPA', 'Neurodevelopmental Disorders-'): 3,
    ('PPA', 'Schizophrenia Spectrum/Other Psychotic Disorders'): 3,
    ('PPA', 'Schizophrenia Spectrum/Other Psychotic Disorders-'): 3,
    ('PPA', 'Bipolar and Depressive Disorders'): 3,
    ('PPA', 'Bipolar and Depressive Disorders-'): 3,
    ('PPA', 'Anxiety Disorders and Obsessive-Compulsive Disorder'): 3,
    ('PPA', 'Anxiety Disorders and Obsessive-Compulsive Disorder-'): 3,
    ('PPA', 'Anxiety Disorders and Obsessive-Compulsive Disorders'): 3,
    ('PPA', 'Trauma/Stressor-Related, Dissociative, and Somatic Symptom Disorders'): 3,
    ('PPA', 'Trauma/Stressor-Related, Dissociative, and Somatic Symptom Disorders-'): 3,
    ('PPA', 'Feeding/Eating, Elimination, and Sleep-Wake Disorders'): 3,
    ('PPA', 'Feeding/Eating, Elimination, and Sleep-Wake Disorders-'): 3,
    ('PPA', 'Feeding/Eating and Sleep-Wake Disorders-'): 3,
    ('PPA', 'Disruptive, Impulse-Control, and Conduct Disorders'): 3,
    ('PPA', 'Disruptive, Impulse-Control, and Conduct Disorders-'): 3,
    ('PPA', 'Substance-Related and Addictive Disorders'): 3,
    ('PPA', 'Substance-Related and Addictive Disorders-'): 3,
    ('PPA', 'Neurocognitive Disorders'): 7,  # v2.2: Moved to D7 (brain-based disorders)
    ('PPA', 'Neurocognitive Disorders-'): 7,  # v2.2: Moved to D7 (brain-based disorders)
    ('PPA', 'Personality Disorders'): 3,
    ('PPA', 'Personality Disorders-'): 3,
    ('PPA', 'Sexual Dysfunctions, Gender Dysphoria, and Paraphilic Disorders'): 3,
    ('PPA', 'Sexual Dysfunctions, Gender Dysphoria, and Paraphilic Disorders-'): 3,

    # CLI mappings
    ('CLI', 'Cognitive-Behavioral Therapies'): 4,
    ('CLI', 'Psychodynamic and Humanistic Therapies'): 4,
    ('CLI', 'Psychodynamic & Humanistic Therapies'): 4,
    ('CLI', 'Family Therapies and Group Therapies'): 4,
    ('CLI', 'Family and Group Therapies'): 4,
    ('CLI', 'Brief Therapies'): 4,
    ('CLI', 'Prevention, Consultation, and Psychotherapy Research'): 4,
    ('CLI', 'Cross-Cultural Issues - Terms and Concepts'): 5,
    ('CLI', 'Cross-Cultural Issues - Identity Development Models'): 5,

    # ETH mappings (v2.1 - split between D8 and D9)
    ('ETH', 'APA Ethics Code Overview and Standards 1 & 2'): 9,
    ('ETH', 'Ethics Code Overview and Standards 1 & 2'): 9,
    ('ETH', 'APA Ethics Code Standards 3 & 4'): 9,
    ('ETH', 'APA Ethics Code Standards 5 & 6'): 9,
    ('ETH', 'Standards 5 & 6'): 9,
    ('ETH', 'APA Ethics Code Standards 7 & 8'): 9,
    ('ETH', 'APA Ethics Code Overview and Standards 7 & 8'): 9,
    ('ETH', 'Standards 7 & 8'): 9,
    ('ETH', 'APA Ethics Code Standards 9 & 10'): 8,  # Moved to D8 in v2.1
    ('ETH', 'Professional Issues'): 8,  # Split - putting in D8 for forensic focus

    # LEA mappings
    ('LEA', 'Classical Conditioning'): 1,
    ('LEA', 'Operant Conditioning'): 1,
    ('LEA', 'Interventions Based on Classical Conditioning'): 4,
    ('LEA', 'Interventions Based on Operant Conditioning'): 4,
    ('LEA', 'Memory and Forgetting'): 7,
    ('LEA', 'Cognitive Factors in Learning'): 7,
}

# v2.8/v2.10/v2.12: Normalize subdomain names to merge duplicates
def normalize_subdomain(subdomain):
    """Normalize subdomain name to handle variations."""
    s = subdomain.strip()
    # Remove trailing hyphens
    s = s.rstrip('-')
    # Normalize ampersand variations
    s = s.replace(' & ', ' and ')
    # Fix capitalization for known issues
    s = s.replace('Endocrine disorders', 'Endocrine Disorders')

    # v2.10: Fix Domain 5 "Bias" vs "Biases" variation
    s = s.replace('Errors, Bias, and Heuristics', 'Errors, Biases, and Heuristics')

    # v2.12: Normalize D2 subdomain variations
    # Fix colon vs hyphen in socioemotional development
    s = s.replace('Socioemotional Development: Temperament and Personality',
                  'Socioemotional Development - Temperament and Personality')
    s = s.replace('Early Influences on Development: Nature vs. Nurture',
                  'Early Influences on Development - Nature vs. Nurture')

    # v2.10: Fix Domain 9 Ethics header variations
    # Normalize all Ethics Standards headers to consistent format
    if 'Standards 1' in s and '2' in s:
        s = 'APA Ethics Code Overview and Standards 1 and 2'
    elif 'Standards 3' in s and '4' in s:
        s = 'APA Ethics Code Standards 3 and 4'
    elif 'Standards 5' in s and '6' in s:
        s = 'APA Ethics Code Standards 5 and 6'
    elif 'Standards 7' in s and '8' in s:
        s = 'APA Ethics Code Standards 7 and 8'
    elif 'Standards 9' in s and '10' in s:
        s = 'APA Ethics Code Standards 9 and 10'

    return s

# Domain names (v2.13 - Updated for uniqueness from ASPPB/PrepJet)
domain_names = {
    1: "Psychometrics & Research Methods",
    2: "Lifespan & Developmental Stages",
    3: "Clinical Psychopathology",
    4: "Psychotherapy Models, Interventions, & Prevention",
    5: "Social & Cultural Psychology",
    6: "Workforce Development & Leadership",
    7: "Biopsychology",
    8: "Clinical Assessment & Interpretation",
    9: "Psychopharmacology & Ethics"
}

# Read CSV and assign domains
domains = {i: [] for i in range(1, 10)}
# v2.9: Track seen content per domain to prevent duplicates
domain_content_seen = {i: set() for i in range(1, 10)}
unassigned = []
duplicates_skipped = 0

csv_path = r'C:\Users\mcdan\Desktop\EPPP_Domain_Design\eppp_exam_questions.csv'
output_dir = r'C:\Users\mcdan\Desktop\EPPP_Domain_Design\anchor_points_by_domain'

# Create output directory
os.makedirs(output_dir, exist_ok=True)

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    for row in reader:
        if len(row) < 10:
            continue

        source = row[5].strip() if len(row) > 5 else ''
        subdomain = row[6].strip() if len(row) > 6 else ''
        anchor_point = row[9].strip() if len(row) > 9 else ''
        question = row[2].strip() if len(row) > 2 else ''
        anchor_id = row[8].strip() if len(row) > 8 else ''

        # v2.8: Fallback to column 7 (full explanation) if column 9 has rewrite error
        if anchor_point == 'Error: Rewrite failed' or not anchor_point:
            anchor_point = row[7].strip() if len(row) > 7 else ''

        if not source or not anchor_point:
            continue

        # Determine domain
        domain = None

        # v2.3: Check anchor-point-level overrides first (highest priority)
        if (source, subdomain, anchor_id) in anchor_point_overrides:
            domain = anchor_point_overrides[(source, subdomain, anchor_id)]
        # Check specific subdomain mapping
        elif (source, subdomain) in specific_mappings:
            domain = specific_mappings[(source, subdomain)]
        # Then check source-level mapping
        elif source in subdomain_mapping:
            domain = subdomain_mapping[source]
        # Handle LIFE typo
        elif source == 'LIFE':
            domain = 2
        elif source == 'PPY':
            domain = 3

        # v2.9: Content-based pharmacology override (for PPA items assigned to D3)
        # Moves pharmacology content from D3 to D9 based on keywords
        if domain == 3 and source == 'PPA' and is_pharmacology_content(anchor_point):
            domain = 9

        # v2.11: Option D - Treatment content migration from D3
        # Route psychosocial treatments to D8, biological treatments to D9
        if domain == 3 and source in ('PPA', 'PPY'):
            if is_biological_treatment(anchor_point):
                domain = 9
            elif is_psychosocial_treatment(anchor_point):
                domain = 8

        if domain:
            # v2.9: Skip duplicate content within same domain
            content_key = anchor_point[:100].lower().strip()
            if content_key in domain_content_seen[domain]:
                duplicates_skipped += 1
            else:
                domain_content_seen[domain].add(content_key)
                # v2.12: Normalize source codes
                normalized_source = 'LIF' if source == 'LIFE' else source
                domains[domain].append({
                    'source': normalized_source,
                    'subdomain': normalize_subdomain(subdomain),  # v2.8: Normalize
                    'anchor_id': anchor_id,
                    'anchor_point': anchor_point,
                    'question': question
                })
        else:
            unassigned.append((source, subdomain, anchor_point[:50]))

# Write each domain to a separate file
for d in range(1, 10):
    filename = f"Domain_{d}_{domain_names[d].replace(' & ', '_').replace(' ', '_')}.txt"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write(f"DOMAIN {d}: {domain_names[d].upper()}\n")
        f.write("=" * 80 + "\n")
        f.write(f"Total Anchor Points: {len(domains[d])}\n")
        f.write("=" * 80 + "\n\n")

        # Group by subdomain
        by_subdomain = {}
        for item in domains[d]:
            key = f"{item['source']}: {item['subdomain']}"
            if key not in by_subdomain:
                by_subdomain[key] = []
            by_subdomain[key].append(item)

        for subdomain_key in sorted(by_subdomain.keys()):
            items = by_subdomain[subdomain_key]
            f.write("-" * 80 + "\n")
            f.write(f"{subdomain_key} ({len(items)} items)\n")
            f.write("-" * 80 + "\n\n")

            # v2.8: Track ID occurrences to disambiguate duplicates
            id_counts = {}
            for item in items:
                aid = item['anchor_id']
                id_counts[aid] = id_counts.get(aid, 0) + 1

            id_seen = {}
            for i, item in enumerate(items, 1):
                aid = item['anchor_id']
                # Add suffix only if this ID appears multiple times
                if id_counts[aid] > 1:
                    id_seen[aid] = id_seen.get(aid, 0) + 1
                    display_id = f"{aid}-{id_seen[aid]}"
                else:
                    display_id = aid
                f.write(f"[{display_id}] {item['anchor_point']}\n\n")

        f.write("\n" + "=" * 80 + "\n")
        f.write("END OF DOMAIN\n")
        f.write("=" * 80 + "\n")

    print(f"Created: {filename} ({len(domains[d])} anchor points)")

# Print summary
print("\n" + "=" * 50)
print("EXPORT SUMMARY")
print("=" * 50)
for d in range(1, 10):
    print(f"Domain {d}: {len(domains[d])} anchor points")
print("-" * 50)
print(f"Total assigned: {sum(len(domains[d]) for d in range(1, 10))}")
print(f"Duplicates skipped: {duplicates_skipped}")
print(f"Unassigned: {len(unassigned)}")

if unassigned:
    print("\nUnassigned items (first 10):")
    for item in unassigned[:10]:
        print(f"  {item[0]}: {item[1]}")
