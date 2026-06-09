#!/usr/bin/env python3
"""Build the comparator pathway gene table for heme biosynthesis (and optionally CoQ).

Fetches Ensembl gene IDs and GRCh38 coordinates via MyGene.info, then writes
data/processed/comparator_gene_table.tsv with the same column schema as
nglyco_gene_table.tsv so that constraint and disease scripts can be reused.

Usage
-----
    python scripts/build_comparator_gene_table.py

Run from the repository root.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd


MYGENE_URL = "https://mygene.info/v3/query"


# ---------------------------------------------------------------------------
# Pathway definitions
# ---------------------------------------------------------------------------

HEME_GENES = [
    # symbol, pathway_step (order), region_label, primary_region, notes
    ("ALAS1", 1, "ala_synthesis_ubiquitous", "core_sequential",
     "5-ALA synthase, ubiquitous isoform. Step 1 committed step.", "high", "OMIM:125290"),
    ("ALAS2", 1, "ala_synthesis_erythroid", "core_sequential",
     "5-ALA synthase, erythroid isoform. Tissue-specific paralog of ALAS1.", "high", "OMIM:301300"),
    ("ALAD",  2, "pbg_synthesis", "core_sequential",
     "ALA dehydratase. Step 2.", "high", "OMIM:125270"),
    ("HMBS",  3, "hydroxymethylbilane_synthesis", "core_sequential",
     "Hydroxymethylbilane synthase. Step 3. Acute intermittent porphyria.", "high", "OMIM:609806"),
    ("UROS",  4, "uro_iii_synthesis", "core_sequential",
     "Uroporphyrinogen III synthase. Step 4. CEP.", "high", "OMIM:606938"),
    ("UROD",  5, "copro_synthesis", "core_sequential",
     "Uroporphyrinogen decarboxylase. Step 5. PCT / HEP.", "high", "OMIM:613521"),
    ("CPOX",  6, "protoporphyrinogen_synthesis", "core_sequential",
     "Coproporphyrinogen oxidase. Step 6. HCP.", "high", "OMIM:121300"),
    ("PPOX",  7, "protoporphyrin_synthesis", "core_sequential",
     "Protoporphyrinogen oxidase. Step 7. VP.", "high", "OMIM:600923"),
    ("FECH",  8, "heme_synthesis", "core_sequential",
     "Ferrochelatase. Step 8. EPP.", "high", "OMIM:177000"),
]

COQ_GENES = [
    ("PDSS1", 1, "decaprenyl_diphosphate", "core_sequential",
     "Decaprenyl diphosphate synthase subunit 1. CoQ isoprenoid tail.", "high", "OMIM:607429"),
    ("PDSS2", 1, "decaprenyl_diphosphate", "core_sequential",
     "Decaprenyl diphosphate synthase subunit 2. CoQ isoprenoid tail.", "high", "OMIM:610564"),
    ("COQ2",  2, "ring_attachment", "core_sequential",
     "4-hydroxybenzoate polyprenyltransferase. Attaches tail to ring.", "high", "OMIM:609825"),
    ("COQ3",  3, "ring_methylation", "core_sequential",
     "Polyprenyldihydroxybenzoate methyltransferase.", "high", "OMIM:614650"),
    ("COQ4",  4, "ring_scaffold", "core_sequential",
     "Coenzyme Q4; structural/scaffold role.", "high", "OMIM:616276"),
    ("COQ5",  5, "ring_methylation_2", "late_modification",
     "Methyltransferase, C-methylation. Less clinically penetrant.", "medium", "OMIM:616359"),
    ("COQ6",  6, "ring_hydroxylation", "late_modification",
     "Monooxygenase, C5-hydroxylation.", "high", "OMIM:614647"),
    ("COQ7",  7, "ring_hydroxylation_2", "late_modification",
     "Monooxygenase, C6-hydroxylation. CABC1 domain.", "high", "OMIM:616500"),
    ("COQ8A", 8, "kinase_atpase", "late_modification",
     "ADCK3; atypical kinase/ATPase. Regulatory.", "high", "OMIM:612016"),
    ("COQ8B", 8, "kinase_atpase", "late_modification",
     "ADCK4; atypical kinase/ATPase. Regulatory.", "high", "OMIM:616538"),
    ("COQ9",  9, "lipid_binding", "late_modification",
     "COQ9; lipid-binding, late assembly.", "high", "OMIM:614647"),
    ("COQ10A", 10, "transport", "late_modification",
     "START domain, CoQ transport/delivery. Less studied.", "low", ""),
    ("COQ10B", 10, "transport", "late_modification",
     "START domain, CoQ transport/delivery. Less studied.", "low", ""),
]


# ---------------------------------------------------------------------------
# MyGene.info lookup
# ---------------------------------------------------------------------------

def fetch_gene_info(symbol: str) -> dict:
    """Fetch Ensembl ID and GRCh38 coordinates from MyGene.info."""
    url = (
        f"https://mygene.info/v3/query?q=symbol:{symbol}&species=human"
        f"&fields=ensembl.gene,genomic_pos_hg19,genomic_pos&size=1"
    )
    try:
        req = Request(url, headers={"Accept": "application/json"})
        with urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
        hits = data.get("hits", [])
        if not hits:
            return {"ensembl_gene_id": None, "grch38_chr": None,
                    "grch38_start": None, "grch38_end": None}
        hit = hits[0]
        ensembl = hit.get("ensembl", {})
        if isinstance(ensembl, list):
            ensembl = ensembl[0]
        eid = ensembl.get("gene")
        gpos = hit.get("genomic_pos", {})
        if isinstance(gpos, list):
            gpos = gpos[0]
        return {
            "ensembl_gene_id": eid,
            "grch38_chr": str(gpos.get("chr", "")) if gpos else None,
            "grch38_start": int(gpos["start"]) if gpos and "start" in gpos else None,
            "grch38_end": int(gpos["end"]) if gpos and "end" in gpos else None,
        }
    except Exception as exc:
        print(f"  [{symbol}] MyGene error: {exc}")
        return {"ensembl_gene_id": None, "grch38_chr": None,
                "grch38_start": None, "grch38_end": None}


# ---------------------------------------------------------------------------
# Build table
# ---------------------------------------------------------------------------

def build_table(gene_definitions: list, pathway_name: str) -> pd.DataFrame:
    records = []
    for defn in gene_definitions:
        symbol, step, pathway_step, primary_region, notes, confidence, omim = defn
        print(f"  Fetching {symbol}...")
        info = fetch_gene_info(symbol)
        records.append({
            "symbol": symbol,
            "ensembl_gene_id": info["ensembl_gene_id"],
            "grch38_chr": info["grch38_chr"],
            "grch38_start": info["grch38_start"],
            "grch38_end": info["grch38_end"],
            "pathway_name": pathway_name,
            "pathway_step_order": step,
            "pathway_step": pathway_step,
            "primary_region": primary_region,
            "analysis_group": primary_region,
            "include_primary": "yes",
            "include_sensitivity": "yes",
            "curation_confidence": confidence,
            "disease_omim": omim,
            "curation_notes": notes,
        })
        time.sleep(0.3)
    return pd.DataFrame(records)


def main() -> None:
    out_path = Path("data/processed/comparator_gene_table.tsv")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print("=== Heme biosynthesis ===")
    heme_df = build_table(HEME_GENES, "heme_biosynthesis")
    print(f"  {len(heme_df)} genes")

    print("\n=== CoQ biosynthesis ===")
    coq_df = build_table(COQ_GENES, "coq_biosynthesis")
    print(f"  {len(coq_df)} genes")

    combined = pd.concat([heme_df, coq_df], ignore_index=True)
    combined.to_csv(out_path, sep="\t", index=False)
    print(f"\nWrote {len(combined)} genes to {out_path}")

    # Quick summary
    print("\nSummary by pathway and region:")
    print(combined.groupby(["pathway_name", "primary_region"]).size().to_string())

    n_eid = int(combined["ensembl_gene_id"].notna().sum())
    print(f"\nEnsembl IDs found: {n_eid}/{len(combined)}")


if __name__ == "__main__":
    main()
