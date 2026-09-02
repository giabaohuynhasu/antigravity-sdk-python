"""
TASK A: FULL 28-YEAR CONSECUTIVE POPULATION CENSUS (1999–2026)
Dataset: cvelistV5 (Every single JSON record across all 28 years)
Author: Gia Bao Huynh (Jun) · Antigravity IDE
"""

import sys
import json
import zipfile
from pathlib import Path
from collections import Counter, defaultdict
import pandas as pd

if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

ZIP_PATH = Path("C:/Users/nswcl/.gemini/antigravity-ide/scratch/cybersecurity-cna-census/data/cybersecurity/cves.zip")
OUTPUT_CSV = Path("C:/Users/nswcl/.gemini/antigravity-ide/scratch/research_replication_package/results/task_a_cna_census_28_years.csv")
OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

def extract_cve_info(raw_bytes):
    try:
        data = json.loads(raw_bytes.decode("utf-8", errors="ignore"))
        cve_meta = data.get("cveMetadata", {})
        state = cve_meta.get("state", "PUBLISHED")
        assigner = cve_meta.get("assignerShortName")
        if not assigner:
            assigner = cve_meta.get("assignerOrgId")
        if not assigner:
            cna_meta = data.get("containers", {}).get("cna", {}).get("providerMetadata", {})
            assigner = cna_meta.get("shortName") or cna_meta.get("orgId")
        return state, (assigner or "UNKNOWN")
    except Exception:
        return "ERROR", "UNKNOWN"

def main():
    print("=" * 80)
    print("TASK A: FULL 28-YEAR POPULATION CENSUS (1999 - 2026)")
    print(f"Source: {ZIP_PATH}")
    print("=" * 80)

    year_total = Counter()
    year_published = Counter()
    year_rejected = Counter()
    year_assigners = defaultdict(Counter)

    processed = 0
    with zipfile.ZipFile(ZIP_PATH, 'r') as z:
        for info in z.infolist():
            if not info.filename.endswith(".json") or "cves/" not in info.filename:
                continue

            parts = info.filename.split("/")
            year_val = None
            for p in parts:
                if p.isdigit() and len(p) == 4:
                    year_val = int(p)
                    break

            if year_val is not None and 1999 <= year_val <= 2026:
                raw_bytes = z.read(info)
                state, assigner = extract_cve_info(raw_bytes)
                year_total[year_val] += 1
                if state == "REJECTED":
                    year_rejected[year_val] += 1
                else:
                    year_published[year_val] += 1
                    year_assigners[year_val][assigner] += 1
                processed += 1
                if processed % 50000 == 0:
                    print(f"  Streaming: processed {processed:,} records...")

    print(f"\n[✓] Completed parsing {processed:,} records across all 28 years.")

    rows = []
    for y in range(1999, 2027):
        tot = year_total[y]
        pub = year_published[y]
        rej = year_rejected[y]
        assigner_counts = year_assigners[y]
        k = len(assigner_counts)

        if pub > 0:
            mitre_count = sum(cnt for name, cnt in assigner_counts.items() if "mitre" in name.lower())
            mitre_share = (mitre_count / pub) * 100.0
            shares = [(cnt / pub) * 100.0 for cnt in assigner_counts.values()]
            sorted_shares = sorted(shares, reverse=True)
            cr10 = sum(sorted_shares[:10])
            hhi = sum(s ** 2 for s in shares)
        else:
            mitre_share, cr10, hhi = 0.0, 0.0, 0.0

        rows.append({
            "year": y,
            "total_records": tot,
            "published_records": pub,
            "rejected_records": rej,
            "rejected_rate_pct": round((rej / tot) * 100.0, 2) if tot > 0 else 0.0,
            "distinct_cnas": k,
            "mitre_published_count": mitre_count if pub > 0 else 0,
            "mitre_direct_share_pct": round(mitre_share, 2),
            "top10_concentration_pct": round(cr10, 2),
            "hhi": round(hhi, 2)
        })

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"\n[✓] Full 28-Year Census CSV saved to: {OUTPUT_CSV}")
    print("\nSummary Table:")
    print(df.to_string(index=False))
    print("\n" + "=" * 80)
    print(f"TOTAL RECORDS (N_all)       : {df['total_records'].sum():,}")
    print(f"TOTAL PUBLISHED (N_pub)     : {df['published_records'].sum():,}")
    print(f"TOTAL REJECTED (N_rej)      : {df['rejected_records'].sum():,} ({df['rejected_records'].sum() / df['total_records'].sum() * 100:.2f}%)")
    print("=" * 80)

if __name__ == '__main__':
    main()
