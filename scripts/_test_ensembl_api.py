#!/usr/bin/env python3
"""Diagnostic: show exact BioMart column names and a few data rows."""
import io, urllib.parse
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import pandas as pd

gene_ids = ["ENSG00000000419", "ENSG00000178802", "ENSG00000140650", "ENSG00000198380"]
ids_str = ",".join(gene_ids)

BIOMART_URL = "https://www.ensembl.org/biomart/martservice?query="

QUERIES = {
    "mouse": f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Query>
<Query virtualSchemaName="default" formatter="TSV" header="1" uniqueRows="1" datasetConfigVersion="0.6">
  <Dataset name="hsapiens_gene_ensembl" interface="default">
    <Filter name="ensembl_gene_id" value="{ids_str}"/>
    <Attribute name="ensembl_gene_id"/>
    <Attribute name="mmusculus_homolog_ensembl_gene"/>
    <Attribute name="mmusculus_homolog_orthology_type"/>
    <Attribute name="mmusculus_homolog_perc_id"/>
    <Attribute name="mmusculus_homolog_perc_id_r1"/>
    <Attribute name="mmusculus_homolog_goc_score"/>
    <Attribute name="mmusculus_homolog_wga_coverage"/>
  </Dataset>
</Query>""",
    "chimp": f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Query>
<Query virtualSchemaName="default" formatter="TSV" header="1" uniqueRows="1" datasetConfigVersion="0.6">
  <Dataset name="hsapiens_gene_ensembl" interface="default">
    <Filter name="ensembl_gene_id" value="{ids_str}"/>
    <Attribute name="ensembl_gene_id"/>
    <Attribute name="ptroglodytes_homolog_ensembl_gene"/>
    <Attribute name="ptroglodytes_homolog_orthology_type"/>
    <Attribute name="ptroglodytes_homolog_perc_id"/>
    <Attribute name="ptroglodytes_homolog_perc_id_r1"/>
    <Attribute name="ptroglodytes_homolog_goc_score"/>
    <Attribute name="ptroglodytes_homolog_wga_coverage"/>
  </Dataset>
</Query>""",
}

for label, xml in QUERIES.items():
    url = BIOMART_URL + urllib.parse.quote(xml)
    print(f"\n{'='*60}")
    print(f"=== {label.upper()} QUERY ===")
    try:
        req = Request(url, headers={"Accept": "text/plain"})
        with urlopen(req, timeout=60) as r:
            raw = r.read().decode("utf-8")

        if raw.startswith("Query ERROR"):
            print("BioMart error:", raw[:400])
        else:
            df = pd.read_csv(io.StringIO(raw), sep="\t")
            print("COLUMNS:")
            for i, c in enumerate(df.columns):
                print(f"  [{i}] {repr(c)}")
            print(f"\nDATA ({len(df)} rows):")
            print(df.to_string())
    except HTTPError as e:
        print(f"HTTPError {e.code}:", e.read().decode()[:300])
    except Exception as e:
        print(f"Error: {e}")
