# Data Directory

Raw genotype and annotation files should not be committed unless they are small, immutable reference tables with a clear license.

For every dataset used, record the source URL or accession, download date, version, genome build, checksum, expected local path, and any filtering or sample-inclusion rules in `docs/methods/`.

Suggested usage:

- `raw/`: downloaded immutable inputs.
- `external/`: small external annotations and reference tables that can be versioned when license-compatible.
- `interim/`: intermediate generated tables.
- `processed/`: final analysis-ready datasets.
