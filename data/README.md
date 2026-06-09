# Data Directory

Raw genotype and annotation files should not be committed unless they are small, immutable reference tables with a clear license.

For every dataset used, record the source URL or accession, download date, version, genome build, checksum, expected local path, and any filtering or sample-inclusion rules in `docs/methods/`.

Suggested usage:

- `raw/`: downloaded immutable inputs.
- `external/`: small external annotations and reference tables that can be versioned when license-compatible.
- `interim/`: intermediate generated tables.
- `processed/`: final analysis-ready datasets.

## gnomAD Constraint Metrics

The provisional constraint run uses the public gnomAD v4.1 constraint metrics TSV:

```text
data/external/gnomad/gnomad.v4.1.constraint_metrics.tsv
```

Download command:

```bash
mkdir -p data/external/gnomad
curl -L \
  -o data/external/gnomad/gnomad.v4.1.constraint_metrics.tsv \
  https://storage.googleapis.com/gcp-public-data--gnomad/release/4.1/constraint/gnomad.v4.1.constraint_metrics.tsv
```

The file is about 96 MB locally and is not committed. Rebuild the project constraint outputs with:

```bash
make constraint-summary \
  CONSTRAINT_METRICS=data/external/gnomad/gnomad.v4.1.constraint_metrics.tsv \
  CONSTRAINT_DATASET_VERSION=gnomAD_v4.1
```

## ClinVar Variant Summary

The disease architecture run uses the public ClinVar tab-delimited variant summary:

```text
data/external/clinvar/variant_summary.txt.gz
```

Download command:

```bash
mkdir -p data/external/clinvar
curl -L \
  -o data/external/clinvar/variant_summary.txt.gz \
  https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/variant_summary.txt.gz
```

The file is about 419 MB locally and is not committed. Rebuild the ClinVar layer with:

```bash
make clinvar-disease-layer \
  CLINVAR_VARIANT_SUMMARY=data/external/clinvar/variant_summary.txt.gz
```

## GWAS Catalog Associations

The complex-trait layer uses the NHGRI-EBI GWAS Catalog v1.0.2 associations download:

```text
data/external/gwas_catalog/gwas_catalog_v1.0.2-associations_e115_r2026-06-01_split.zip
```

Download command:

```bash
mkdir -p data/external/gwas_catalog
curl -L \
  -o data/external/gwas_catalog/gwas_catalog_v1.0.2-associations_e115_r2026-06-01_split.zip \
  'https://www.ebi.ac.uk/gwas/api/search/downloads/associations/v1.0.2'
```

The archive is about 63 MB locally and is not committed. Rebuild the GWAS trait layer with:

```bash
make gwas-trait-layer \
  GWAS_CATALOG_ASSOCIATIONS=data/external/gwas_catalog/gwas_catalog_v1.0.2-associations_e115_r2026-06-01_split.zip
```
