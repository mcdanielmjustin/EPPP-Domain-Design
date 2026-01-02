import csv
import os

# v2.3: Anchor-point-level overrides (highest priority)
# Format: (source, subdomain, anchor_id) -> domain
anchor_point_overrides = {
    # Pharmacology content moved from D3 to D9
    ('PPA', 'Neurodevelopmental Disorders', '03'): 9,  # Antipsychotics for tics
    ('PPA', 'Sexual Dysfunctions, Gender Dysphoria, and Paraphilic Disorders', '21'): 9,  # Serotonin for PE
    ('PPA', 'Bipolar and Depressive Disorders', '27'): 9,  # St. John's wort + SSRI
    ('PPA', 'Bipolar and Depressive Disorders', '157'): 9,  # St. John's wort comparison
}

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

# Domain names
domain_names = {
    1: "Psychometrics & Scientific Foundations",
    2: "Developmental Psychology",
    3: "Clinical Psychopathology",
    4: "Therapeutic Psychology",
    5: "Social & Cultural Psychology",
    6: "Organizational Psychology",
    7: "Biopsychology",
    8: "Psychological Assessment",
    9: "Psychopharmacology & Professional Ethics"
}

# Read CSV and assign domains
domains = {i: [] for i in range(1, 10)}
unassigned = []

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

        if domain:
            domains[domain].append({
                'source': source,
                'subdomain': subdomain,
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

            for i, item in enumerate(items, 1):
                f.write(f"[{item['anchor_id']}] {item['anchor_point']}\n\n")

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
print(f"Unassigned: {len(unassigned)}")

if unassigned:
    print("\nUnassigned items (first 10):")
    for item in unassigned[:10]:
        print(f"  {item[0]}: {item[1]}")
