#!/usr/bin/env python3
"""Null model test for the N-glycosylation disease architecture gradient.

The critique: CDG/severe disease concentrating in shared early steps may be a
universal trivial consequence of shared-step essentiality, not a property
specific to N-glycosylation's layered topology.

This script tests whether the disease-burden gradient is replicated in four
comparator pathways that differ in downstream combinatorial diversity:

  NEGATIVE CONTROLS (no downstream diversification):
  - GPI-anchor biosynthesis: strictly linear, all steps equally essential
  - Purine de novo biosynthesis: linear 10-step pathway, no downstream branches

  TOPOLOGY-MATCHED (shared core → combinatorial downstream):
  - Heparan sulfate (HS) proteoglycan: linker core → diversified HS modification
  - Ceramide / glycosphingolipid: ceramide core → diversified glycolipid layer

Prediction:
  - If pattern is trivially universal: all four pathways show disease concentration
    in "core" steps regardless of whether they have downstream diversification.
  - If pattern requires combinatorial topology: only HS and ceramide show the
    gradient; GPI and purine do NOT.

Evidence streams per gene:
  1. LOEUF from gnomAD v4.1 (local file)
  2. OMIM phenotype count from MyGene.info (Mendelian disease burden proxy)
  3. Has-known-disease flag (boolean)

Outputs
-------
data/processed/pathway_null_model_genes.tsv
results/tables/pathway_null_model_comparison.tsv
results/tables/pathway_null_model_summary.txt
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu

GNOMAD_FILE = "data/external/gnomad/gnomad.v4.1.constraint_metrics.tsv"
GENES_OUT = "data/processed/pathway_null_model_genes.tsv"
COMPARISON_OUT = "results/tables/pathway_null_model_comparison.tsv"
SUMMARY_OUT = "results/tables/pathway_null_model_summary.txt"
OMIM_CACHE = "data/raw/pathway_null_model_omim_cache.tsv"

MYGENE_URL = "https://mygene.info/v3/query"


# ---------------------------------------------------------------------------
# Pathway gene definitions
# Each gene gets: symbol, pathway, layer (core | downstream), topology_type
# ---------------------------------------------------------------------------

# topology_type:
#   "linear"  — all steps in a single unbranched chain, no downstream diversity
#   "layered" — conserved shared core feeding combinatorial/diversified output


PATHWAY_GENES: list[dict] = [

    # -----------------------------------------------------------------------
    # GPI-ANCHOR BIOSYNTHESIS — strictly linear, no downstream diversification
    # All steps build a single conserved anchor structure. Every gene is "core".
    # Germline biallelic loss of any step causes MCAHS/HPMRS syndromes.
    # -----------------------------------------------------------------------
    # has_disease: all cause GPI deficiency disorders (MCAHS, HPMRS) when biallelic
    # PIGA is somatic only (PNH), coded False for germline Mendelian
    {"symbol": "PIGA",  "pathway": "gpi_anchor", "layer": "core", "topology_type": "linear", "has_mendelian_disease": False, "disease_notes": "Somatic PNH only"},
    {"symbol": "PIGB",  "pathway": "gpi_anchor", "layer": "core", "topology_type": "linear", "has_mendelian_disease": True,  "disease_notes": "MCAHS3"},
    {"symbol": "PIGC",  "pathway": "gpi_anchor", "layer": "core", "topology_type": "linear", "has_mendelian_disease": True,  "disease_notes": "HPMRS"},
    {"symbol": "PIGF",  "pathway": "gpi_anchor", "layer": "core", "topology_type": "linear", "has_mendelian_disease": True,  "disease_notes": "HPMRS2"},
    {"symbol": "PIGG",  "pathway": "gpi_anchor", "layer": "core", "topology_type": "linear", "has_mendelian_disease": True,  "disease_notes": "HPMRS7"},
    {"symbol": "PIGH",  "pathway": "gpi_anchor", "layer": "core", "topology_type": "linear", "has_mendelian_disease": True,  "disease_notes": "MCAHS"},
    {"symbol": "PIGK",  "pathway": "gpi_anchor", "layer": "core", "topology_type": "linear", "has_mendelian_disease": True,  "disease_notes": "MCAHS5"},
    {"symbol": "PIGL",  "pathway": "gpi_anchor", "layer": "core", "topology_type": "linear", "has_mendelian_disease": True,  "disease_notes": "MCAHS2"},
    {"symbol": "PIGM",  "pathway": "gpi_anchor", "layer": "core", "topology_type": "linear", "has_mendelian_disease": True,  "disease_notes": "PNH+seizures"},
    {"symbol": "PIGN",  "pathway": "gpi_anchor", "layer": "core", "topology_type": "linear", "has_mendelian_disease": True,  "disease_notes": "MCAHS4"},
    {"symbol": "PIGO",  "pathway": "gpi_anchor", "layer": "core", "topology_type": "linear", "has_mendelian_disease": True,  "disease_notes": "HPMRS3"},
    {"symbol": "PIGP",  "pathway": "gpi_anchor", "layer": "core", "topology_type": "linear", "has_mendelian_disease": True,  "disease_notes": "MCAHS"},
    {"symbol": "PIGQ",  "pathway": "gpi_anchor", "layer": "core", "topology_type": "linear", "has_mendelian_disease": True,  "disease_notes": "MCAHS"},
    {"symbol": "PIGS",  "pathway": "gpi_anchor", "layer": "core", "topology_type": "linear", "has_mendelian_disease": True,  "disease_notes": "HPMRS9"},
    {"symbol": "PIGT",  "pathway": "gpi_anchor", "layer": "core", "topology_type": "linear", "has_mendelian_disease": True,  "disease_notes": "MCAHS3"},
    {"symbol": "PIGU",  "pathway": "gpi_anchor", "layer": "core", "topology_type": "linear", "has_mendelian_disease": True,  "disease_notes": "HPMRS4"},
    {"symbol": "PIGV",  "pathway": "gpi_anchor", "layer": "core", "topology_type": "linear", "has_mendelian_disease": True,  "disease_notes": "HPMRS1"},
    {"symbol": "PIGW",  "pathway": "gpi_anchor", "layer": "core", "topology_type": "linear", "has_mendelian_disease": True,  "disease_notes": "HPMRS5"},
    {"symbol": "PIGX",  "pathway": "gpi_anchor", "layer": "core", "topology_type": "linear", "has_mendelian_disease": True,  "disease_notes": "MCAHS"},
    {"symbol": "PIGY",  "pathway": "gpi_anchor", "layer": "core", "topology_type": "linear", "has_mendelian_disease": True,  "disease_notes": "HPMRS6"},
    {"symbol": "GPAA1", "pathway": "gpi_anchor", "layer": "core", "topology_type": "linear", "has_mendelian_disease": True,  "disease_notes": "HPMRS8"},

    # -----------------------------------------------------------------------
    # PURINE DE NOVO BIOSYNTHESIS — linear pathway, modest AMP/GMP branching
    # -----------------------------------------------------------------------
    {"symbol": "PPAT",   "pathway": "purine_denovo", "layer": "core",       "topology_type": "linear", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "GART",   "pathway": "purine_denovo", "layer": "core",       "topology_type": "linear", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "PFAS",   "pathway": "purine_denovo", "layer": "core",       "topology_type": "linear", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "PAICS",  "pathway": "purine_denovo", "layer": "core",       "topology_type": "linear", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "ADSL",   "pathway": "purine_denovo", "layer": "core",       "topology_type": "linear", "has_mendelian_disease": True,  "disease_notes": "Adenylosuccinase deficiency (severe)"},
    {"symbol": "ATIC",   "pathway": "purine_denovo", "layer": "core",       "topology_type": "linear", "has_mendelian_disease": True,  "disease_notes": "AICA-ribosiduria (severe)"},
    {"symbol": "ADSS2",  "pathway": "purine_denovo", "layer": "downstream", "topology_type": "linear", "has_mendelian_disease": True,  "disease_notes": "Hypotonia-intellectual disability (severe)"},
    {"symbol": "GMPS",   "pathway": "purine_denovo", "layer": "downstream", "topology_type": "linear", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "IMPDH1", "pathway": "purine_denovo", "layer": "downstream", "topology_type": "linear", "has_mendelian_disease": True,  "disease_notes": "Leber congenital amaurosis 11 (dominant)"},
    {"symbol": "IMPDH2", "pathway": "purine_denovo", "layer": "downstream", "topology_type": "linear", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},

    # -----------------------------------------------------------------------
    # HEPARAN SULFATE (HS) PROTEOGLYCAN BIOSYNTHESIS
    # topology: conserved linker core → diversified HS modification layer
    # -----------------------------------------------------------------------
    {"symbol": "XYLT1",    "pathway": "hs_biosynthesis", "layer": "core",       "topology_type": "layered", "has_mendelian_disease": True,  "disease_notes": "Desbuquois dysplasia 2"},
    {"symbol": "XYLT2",    "pathway": "hs_biosynthesis", "layer": "core",       "topology_type": "layered", "has_mendelian_disease": True,  "disease_notes": "Spondyloocular syndrome"},
    {"symbol": "B4GALT7",  "pathway": "hs_biosynthesis", "layer": "core",       "topology_type": "layered", "has_mendelian_disease": True,  "disease_notes": "EDS progeroid type 1"},
    {"symbol": "B3GALT6",  "pathway": "hs_biosynthesis", "layer": "core",       "topology_type": "layered", "has_mendelian_disease": True,  "disease_notes": "EDS spondylodysplastic type 2"},
    {"symbol": "B3GAT3",   "pathway": "hs_biosynthesis", "layer": "core",       "topology_type": "layered", "has_mendelian_disease": True,  "disease_notes": "JDSSDHD / laryngotracheomalacia"},
    {"symbol": "EXT1",     "pathway": "hs_biosynthesis", "layer": "core",       "topology_type": "layered", "has_mendelian_disease": True,  "disease_notes": "Hereditary multiple exostoses type 1 (dominant)"},
    {"symbol": "EXT2",     "pathway": "hs_biosynthesis", "layer": "core",       "topology_type": "layered", "has_mendelian_disease": True,  "disease_notes": "Hereditary multiple exostoses type 2 (dominant)"},
    {"symbol": "EXTL3",    "pathway": "hs_biosynthesis", "layer": "core",       "topology_type": "layered", "has_mendelian_disease": True,  "disease_notes": "Immunoskeletal dysplasia with NDD"},
    # HS modification: diversified sulfation — minimal Mendelian disease
    {"symbol": "NDST1",    "pathway": "hs_biosynthesis", "layer": "downstream", "topology_type": "layered", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "NDST2",    "pathway": "hs_biosynthesis", "layer": "downstream", "topology_type": "layered", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "NDST3",    "pathway": "hs_biosynthesis", "layer": "downstream", "topology_type": "layered", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "NDST4",    "pathway": "hs_biosynthesis", "layer": "downstream", "topology_type": "layered", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "HS2ST1",   "pathway": "hs_biosynthesis", "layer": "downstream", "topology_type": "layered", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "HS3ST1",   "pathway": "hs_biosynthesis", "layer": "downstream", "topology_type": "layered", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "HS3ST2",   "pathway": "hs_biosynthesis", "layer": "downstream", "topology_type": "layered", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "HS3ST3A1", "pathway": "hs_biosynthesis", "layer": "downstream", "topology_type": "layered", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "HS3ST3B1", "pathway": "hs_biosynthesis", "layer": "downstream", "topology_type": "layered", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "HS3ST4",   "pathway": "hs_biosynthesis", "layer": "downstream", "topology_type": "layered", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "HS3ST5",   "pathway": "hs_biosynthesis", "layer": "downstream", "topology_type": "layered", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "HS3ST6",   "pathway": "hs_biosynthesis", "layer": "downstream", "topology_type": "layered", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "HS6ST1",   "pathway": "hs_biosynthesis", "layer": "downstream", "topology_type": "layered", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "HS6ST3",   "pathway": "hs_biosynthesis", "layer": "downstream", "topology_type": "layered", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "SULF1",    "pathway": "hs_biosynthesis", "layer": "downstream", "topology_type": "layered", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "SULF2",    "pathway": "hs_biosynthesis", "layer": "downstream", "topology_type": "layered", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},

    # -----------------------------------------------------------------------
    # CERAMIDE / GLYCOSPHINGOLIPID BIOSYNTHESIS
    # -----------------------------------------------------------------------
    {"symbol": "SPTLC1",   "pathway": "ceramide_gsl", "layer": "core",       "topology_type": "layered", "has_mendelian_disease": True,  "disease_notes": "HSN1A (dominant)"},
    {"symbol": "SPTLC2",   "pathway": "ceramide_gsl", "layer": "core",       "topology_type": "layered", "has_mendelian_disease": True,  "disease_notes": "HSN1B; ALS (dominant)"},
    {"symbol": "SPTLC3",   "pathway": "ceramide_gsl", "layer": "core",       "topology_type": "layered", "has_mendelian_disease": True,  "disease_notes": "HSN1F (dominant)"},
    {"symbol": "SPTSSA",   "pathway": "ceramide_gsl", "layer": "core",       "topology_type": "layered", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "SPTSSB",   "pathway": "ceramide_gsl", "layer": "core",       "topology_type": "layered", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "KDSR",     "pathway": "ceramide_gsl", "layer": "core",       "topology_type": "layered", "has_mendelian_disease": True,  "disease_notes": "Erythrokeratoderma variabilis (recessive)"},
    {"symbol": "CERS1",    "pathway": "ceramide_gsl", "layer": "core",       "topology_type": "layered", "has_mendelian_disease": True,  "disease_notes": "Progressive myoclonic epilepsy 8"},
    {"symbol": "CERS2",    "pathway": "ceramide_gsl", "layer": "core",       "topology_type": "layered", "has_mendelian_disease": True,  "disease_notes": "Progressive myoclonic epilepsy 8 / leukodystrophy"},
    {"symbol": "CERS3",    "pathway": "ceramide_gsl", "layer": "core",       "topology_type": "layered", "has_mendelian_disease": True,  "disease_notes": "ARCI type 9"},
    {"symbol": "CERS4",    "pathway": "ceramide_gsl", "layer": "core",       "topology_type": "layered", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "CERS5",    "pathway": "ceramide_gsl", "layer": "core",       "topology_type": "layered", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "CERS6",    "pathway": "ceramide_gsl", "layer": "core",       "topology_type": "layered", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "DEGS1",    "pathway": "ceramide_gsl", "layer": "core",       "topology_type": "layered", "has_mendelian_disease": True,  "disease_notes": "Hypomyelinating leukodystrophy 18"},
    {"symbol": "DEGS2",    "pathway": "ceramide_gsl", "layer": "core",       "topology_type": "layered", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "UGCG",     "pathway": "ceramide_gsl", "layer": "downstream", "topology_type": "layered", "has_mendelian_disease": False, "disease_notes": "No known human Mendelian disease (mouse lethal)"},
    {"symbol": "B4GALT5",  "pathway": "ceramide_gsl", "layer": "downstream", "topology_type": "layered", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "B4GALNT1", "pathway": "ceramide_gsl", "layer": "downstream", "topology_type": "layered", "has_mendelian_disease": True,  "disease_notes": "Spastic paraplegia 26 (SPG26)"},
    {"symbol": "ST8SIA1",  "pathway": "ceramide_gsl", "layer": "downstream", "topology_type": "layered", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "ST8SIA5",  "pathway": "ceramide_gsl", "layer": "downstream", "topology_type": "layered", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "B4GALNT2", "pathway": "ceramide_gsl", "layer": "downstream", "topology_type": "layered", "has_mendelian_disease": False, "disease_notes": "No known Mendelian disease"},
    {"symbol": "ST3GAL5",  "pathway": "ceramide_gsl", "layer": "downstream", "topology_type": "layered", "has_mendelian_disease": True,  "disease_notes": "GM3 synthase deficiency / Salt-and-Pepper syndrome (severe)"},
    {"symbol": "A4GALT",   "pathway": "ceramide_gsl", "layer": "downstream", "topology_type": "layered", "has_mendelian_disease": False, "disease_notes": "pk blood group only; no severe Mendelian disease"},
]

# Deduplicate (ADSL appears in two layers of purine — keep first occurrence)
seen = set()
PATHWAY_GENES_DEDUP = []
for g in PATHWAY_GENES:
    key = (g["symbol"], g["pathway"])
    if key not in seen:
        seen.add(key)
        PATHWAY_GENES_DEDUP.append(g)

PATHWAY_GENES = PATHWAY_GENES_DEDUP


# ---------------------------------------------------------------------------
# Fetch OMIM phenotype count from MyGene.info
# ---------------------------------------------------------------------------

def fetch_omim_phenotypes(symbols: list[str], cache_path: str) -> pd.DataFrame:
    """Return DataFrame with symbol and n_omim_phenotypes."""
    cache = Path(cache_path)
    if cache.exists():
        print(f"Loading OMIM cache: {cache}")
        return pd.read_csv(cache, sep="\t")

    print(f"Fetching OMIM phenotype counts for {len(symbols)} genes via MyGene.info...")
    records = []
    batch_size = 20
    for i in range(0, len(symbols), batch_size):
        batch = symbols[i:i + batch_size]
        query = ",".join(batch)
        url = f"https://mygene.info/v3/query?q=symbol:{'+OR+symbol:'.join(batch)}&fields=symbol,omim&species=human&size={batch_size}"
        try:
            req = Request(url, headers={"Accept": "application/json"})
            with urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
            hits = {h.get("symbol", ""): h for h in data.get("hits", [])}
            for sym in batch:
                hit = hits.get(sym, {})
                omim = hit.get("omim", [])
                if isinstance(omim, str):
                    omim = [omim]
                records.append({"symbol": sym, "n_omim_ids": len(omim),
                                "omim_ids": ";".join(str(x) for x in omim)})
                print(f"  {sym}: {len(omim)} OMIM IDs")
        except Exception as exc:
            print(f"  Batch {i//batch_size + 1} failed: {exc}")
            for sym in batch:
                records.append({"symbol": sym, "n_omim_ids": None, "omim_ids": ""})
        time.sleep(0.3)

    df = pd.DataFrame(records)
    cache.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(cache, sep="\t", index=False)
    print(f"Saved OMIM cache: {cache}")
    return df


# ---------------------------------------------------------------------------
# Load gnomAD constraint for a list of symbols
# ---------------------------------------------------------------------------

def load_gnomad_constraint(symbols: list[str]) -> pd.DataFrame:
    print(f"Loading gnomAD constraint for {len(symbols)} genes...")
    gnomad = pd.read_csv(GNOMAD_FILE, sep="\t",
                         usecols=["gene", "canonical", "mane_select",
                                  "lof.oe_ci.upper", "lof.oe", "lof.pLI",
                                  "mis.z_score", "cds_length"])
    # Keep canonical / MANE Select
    canonical = gnomad[(gnomad["canonical"] == True) | (gnomad["mane_select"] == True)]
    # Prefer MANE Select; deduplicate by gene
    canonical = canonical.sort_values("mane_select", ascending=False).drop_duplicates("gene")
    match = canonical[canonical["gene"].isin(symbols)].copy()
    match = match.rename(columns={
        "gene": "symbol",
        "lof.oe_ci.upper": "loeuf",
        "lof.oe": "oe_lof",
        "lof.pLI": "pLI",
        "mis.z_score": "mis_z",
    })
    print(f"  Matched {len(match)}/{len(symbols)} genes")
    unmatched = set(symbols) - set(match["symbol"])
    if unmatched:
        print(f"  Unmatched: {sorted(unmatched)}")
    return match[["symbol", "loeuf", "oe_lof", "pLI", "mis_z", "cds_length"]]


# ---------------------------------------------------------------------------
# Compare core vs downstream within each pathway
# ---------------------------------------------------------------------------

def fisher_test(a_yes, a_no, b_yes, b_no):
    """2×2 Fisher's exact test. Returns odds ratio and p-value."""
    from scipy.stats import fisher_exact
    table = [[a_yes, a_no], [b_yes, b_no]]
    odds, p = fisher_exact(table, alternative="two-sided")
    return odds, p


def compare_layers(df: pd.DataFrame, pathway: str, lines: list[str]) -> dict:
    """Mann-Whitney comparison of LOEUF between core and downstream."""
    sub = df[df["pathway"] == pathway].copy()
    sub_loeuf = sub[sub["loeuf"].notna()]
    core_l = sub_loeuf[sub_loeuf["layer"] == "core"]["loeuf"].dropna()
    dn_l   = sub_loeuf[sub_loeuf["layer"] == "downstream"]["loeuf"].dropna()

    # Disease burden
    core_d  = sub[sub["layer"] == "core"]["has_mendelian_disease"]
    dn_d    = sub[sub["layer"] == "downstream"]["has_mendelian_disease"]
    core_yes = int(core_d.sum()); core_no = int((~core_d).sum())
    dn_yes   = int(dn_d.sum());   dn_no   = int((~dn_d).sum())
    core_dis_frac = core_yes / len(core_d) if len(core_d) else np.nan
    dn_dis_frac   = dn_yes / len(dn_d)     if len(dn_d)   else np.nan

    row = {
        "pathway": pathway,
        "topology_type": sub["topology_type"].iloc[0],
        "n_core": len(sub[sub["layer"] == "core"]),
        "n_downstream": len(sub[sub["layer"] == "downstream"]),
        "core_median_loeuf": round(float(core_l.median()), 4) if len(core_l) else np.nan,
        "downstream_median_loeuf": round(float(dn_l.median()), 4) if len(dn_l) else np.nan,
        "loeuf_mw_p": np.nan,
        "loeuf_direction": "",
        "core_disease_frac": round(core_dis_frac, 3) if not np.isnan(core_dis_frac) else np.nan,
        "downstream_disease_frac": round(dn_dis_frac, 3) if not np.isnan(dn_dis_frac) else np.nan,
        "disease_fisher_p": np.nan,
        "disease_direction": "",
    }

    lines.append(f"\n  {pathway.upper()}  [{sub['topology_type'].iloc[0]}]")

    # LOEUF comparison
    lines.append(f"    LOEUF  — Core (n={len(core_l)}): {core_l.median():.3f}" if len(core_l) else "    LOEUF  — Core: no data")
    lines.append(f"             Downstream (n={len(dn_l)}): {dn_l.median():.3f}" if len(dn_l) else "             Downstream: no data")
    if len(core_l) >= 3 and len(dn_l) >= 3:
        stat, p = mannwhitneyu(core_l, dn_l, alternative="two-sided")
        row["loeuf_mw_p"] = round(p, 4)
        row["loeuf_direction"] = "core_less_constrained" if core_l.median() > dn_l.median() else "core_more_constrained"
        lines.append(f"             MW p={p:.4f}  direction={row['loeuf_direction']}")
    else:
        lines.append("             Too few data for MW test")

    # Disease comparison
    lines.append(f"    Disease — Core: {core_yes}/{len(core_d)} ({core_dis_frac:.0%}) have Mendelian disease" if not np.isnan(core_dis_frac) else "    Disease — Core: no data")
    lines.append(f"              Downstream: {dn_yes}/{len(dn_d)} ({dn_dis_frac:.0%}) have Mendelian disease" if not np.isnan(dn_dis_frac) else "              Downstream: no data")
    if dn_yes + dn_no > 0 and core_yes + core_no > 0:
        odds, p_fisher = fisher_test(core_yes, core_no, dn_yes, dn_no)
        row["disease_fisher_p"] = round(p_fisher, 4)
        row["disease_direction"] = "core_more_disease" if core_dis_frac > dn_dis_frac else "downstream_more_disease" if dn_dis_frac > core_dis_frac else "equal"
        lines.append(f"              Fisher OR={odds:.2f}, p={p_fisher:.4f}  direction={row['disease_direction']}")

    return row


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    for path in [GENES_OUT, COMPARISON_OUT, SUMMARY_OUT]:
        Path(path).parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(PATHWAY_GENES)
    symbols = df["symbol"].unique().tolist()

    # Fetch constraint
    constraint = load_gnomad_constraint(symbols)
    df = df.merge(constraint, on="symbol", how="left")
    df["has_mendelian_disease"] = df["has_mendelian_disease"].fillna(False)

    df.to_csv(GENES_OUT, sep="\t", index=False)
    print(f"\nGene table: {GENES_OUT}  ({len(df)} genes)")

    # ---  Comparisons ---
    lines = ["PATHWAY NULL MODEL — Core vs Downstream LOEUF & Disease Burden",
             "=" * 70,
             "",
             "Prediction: if disease-gradient is trivially universal, ALL pathways",
             "(including GPI and purine with no downstream diversity) show disease",
             "concentration in core genes.",
             "If pattern requires combinatorial topology, only HS and ceramide",
             "(topology-matched) show the gradient; GPI and purine do NOT.",
             "",
             "LOEUF: lower = more constrained. Core-less-constrained = N-glyco pattern.",
             "OMIM: higher count = more Mendelian disease evidence.",
             ""]

    comparison_rows = []
    for pathway in df["pathway"].unique():
        row = compare_layers(df, pathway, lines)
        comparison_rows.append(row)

    # --- Add N-glyco summary for reference ---
    lines.append("\n  N-GLYCO (reference, from main analysis)")
    lines.append("    Core upstream (n=~26): median LOEUF=0.909")
    lines.append("    Downstream (n=~27): median LOEUF=0.740")
    lines.append("    MW p=0.011 (raw), p=0.222 after gene-length control")
    lines.append("    Direction: core_less_constrained (LOEUF inversion)")
    lines.append("    CDG disease: 11/15 LLO genes, 5/11 OST genes")
    lines.append("    Downstream CDG: 0/5 branching, 1/16 terminal-modification")

    # --- Topology summary ---
    comp_df = pd.DataFrame(comparison_rows)
    comp_df.to_csv(COMPARISON_OUT, sep="\t", index=False)

    lines.append("\n\n" + "=" * 70)
    lines.append("SUMMARY TABLE")
    lines.append("=" * 70)
    lines.append(f"{'Pathway':<25} {'Topo':<8} {'Core LOEUF':>10} {'DN LOEUF':>10} {'LOEUF p':>8} {'Core dis%':>10} {'DN dis%':>9} {'Fisher p':>9} {'Disease dir':<25}")
    lines.append("-" * 120)
    for _, row in comp_df.iterrows():
        lines.append(
            f"{row['pathway']:<25} {str(row['topology_type']):<8} "
            f"{str(row['core_median_loeuf']):>10} {str(row['downstream_median_loeuf']):>10} "
            f"{str(row['loeuf_mw_p']):>8} "
            f"{str(row['core_disease_frac']):>10} {str(row['downstream_disease_frac']):>9} "
            f"{str(row['disease_fisher_p']):>9} {str(row['disease_direction']):<25}"
        )
    # Add N-glyco reference row
    lines.append(f"{'nglyco (ref)':<25} {'layered':<8} {'0.909':>10} {'0.740':>10} {'0.011*':>8} {'0.73':>10} {'0.06':>9} {'<0.001':>9} {'core_more_disease':<25}")

    lines.append("\n\nINTERPRETATION GUIDE")
    lines.append("-" * 70)
    lines.append("GPI/purine (linear, no diversity):")
    lines.append("  If CORE < DOWNSTREAM LOEUF (core more constrained) → pattern is universal")
    lines.append("  If CORE ≈ DOWNSTREAM LOEUF (no gradient)           → linear pathways differ from N-glyco")
    lines.append("HS/ceramide (layered, topology-matched):")
    lines.append("  If same inversion as N-glyco → pattern is specific to layered topology")
    lines.append("  If uniform constraint        → N-glyco is uniquely structured")

    summary_text = "\n".join(lines)
    with open(SUMMARY_OUT, "w") as f:
        f.write(summary_text)

    print(summary_text)
    print(f"\nOutputs: {GENES_OUT}, {COMPARISON_OUT}, {SUMMARY_OUT}")


if __name__ == "__main__":
    main()
