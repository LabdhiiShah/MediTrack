import re
import itertools


# already known pairs
# These are clinically significant interactions — scored immediately as HIGH
KNOWN_PAIRS = {
    frozenset({"warfarin", "aspirin"}):       ("HIGH",     0.95, "Increased bleeding risk"),
    frozenset({"warfarin", "ibuprofen"}):     ("HIGH",     0.90, "Increased bleeding risk"),
    frozenset({"warfarin", "naproxen"}):      ("HIGH",     0.88, "Increased bleeding risk"),
    frozenset({"aspirin", "ibuprofen"}):      ("MODERATE", 0.65, "Reduced aspirin efficacy + GI risk"),
    frozenset({"metformin", "contrast dye"}): ("HIGH",     0.85, "Risk of lactic acidosis"),
    frozenset({"lisinopril", "spironolactone"}): ("MODERATE", 0.60, "Hyperkalemia risk"),
    frozenset({"amiodarone", "warfarin"}):    ("HIGH",     0.92, "Elevated anticoagulation effect"),
    frozenset({"aspirin", "warfarin"}):       ("HIGH",     0.95, "Increased bleeding risk"),
    frozenset({"paracetamol", "warfarin"}):   ("MODERATE", 0.55, "Enhanced anticoagulation at high doses"),
}


def _extract_salts(salt_str: str) -> set:
    """Extract meaningful words (4+ chars) from a salt composition string."""
    return set(re.findall(r'[a-zA-Z]{4,}', salt_str.lower()))


def score_all(med_list: list) -> list:
    """
    Score all pairs of medicines for interactions.
    Priority:
      1. Known dangerous pair → immediate HIGH/MODERATE
      2. Shared salt ingredients → score += 50
      3. Overlapping tags       → score += 30
    """
    results = []

    for med1, med2 in itertools.combinations(med_list, 2):
        score   = 0
        reasons = []
        source  = "analysis_engine"

        g1 = (med1.get('generic') or med1['name']).lower()
        g2 = (med2.get('generic') or med2['name']).lower()

        pair_key = frozenset({g1, g2})
        if pair_key in KNOWN_PAIRS:
            level, raw_score, reason = KNOWN_PAIRS[pair_key]
            results.append({
                "medicine_1": med1['name'],
                "medicine_2": med2['name'],
                "risk_score": raw_score,
                "risk_level": level,
                "reasons":    [reason],
                "source":     "known_interaction",
            })
            continue

       # salt composition factor 
        s1 = _extract_salts(med1.get('salt', ''))
        s2 = _extract_salts(med2.get('salt', ''))
        common_salts = s1 & s2

        if common_salts:
            score += 50
            reasons.append(f"Shared ingredients: {', '.join(sorted(common_salts))}")
            source = "shared_salt"

        # redundant tags
        t1 = set(med1.get('tags', '').split(',')) - {''}
        t2 = set(med2.get('tags', '').split(',')) - {''}
        common_tags = t1 & t2

        if common_tags:
            score += 30
            reasons.append(f"Overlapping effects: {', '.join(sorted(common_tags))}")
            source = source if source == "shared_salt" else "dataset_lookup"

        #counting score 
        if score > 0:
            if score >= 70:
                level = "HIGH"
            elif score >= 40:
                level = "MODERATE"
            else:
                level = "LOW"

            results.append({
                "medicine_1": med1['name'],
                "medicine_2": med2['name'],
                "risk_score": round(score / 100, 2),
                "risk_level": level,
                "reasons":    reasons,
                "source":     source,
            })

    # descending order
    results.sort(key=lambda x: x['risk_score'], reverse=True)
    return results