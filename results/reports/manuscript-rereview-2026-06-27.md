# Pre-submission Manuscript Re-review

Date: 2026-06-27

Manuscript: `docs/manuscript/draft.md`

## Editorial decision

**Major revision before submission, but not major new analysis.** The paper now has a coherent and potentially publishable core: severe disease and cell-line fitness costs concentrate in shared upstream machinery, whereas currently assigned glycan-output trait associations concentrate downstream. The negative coding-constraint, dN/dS, and population-genetic results usefully narrow the claim. The remaining work is mainly to align the title and conclusions with what is measured, complete the submission package, and remove several statements that are stronger than the analyses permit.

## What is working

1. **The paper has a distinct question.** It asks whether pathway position separates catastrophic disruption from tolerated quantitative output variation, rather than repeating the 2012 selection scan.
2. **The strongest result is orthogonal across evidence types.** Curated CDG/ClinVar burden and DepMap fitness costs both point to greater disruption cost upstream, while IgG glycan locus assignments point downstream.
3. **Negative results are reported honestly.** LOEUF, pairwise dN/dS, FST, and iHS do not show a simple upstream/downstream evolutionary gradient.
4. **The manuscript anticipates the obvious objections.** It explicitly separates GWAS assignment from causality and coding conservation from evolvability.
5. **The study is reproducible enough to support review.** Scripts, evidence tables, data versions, and a reproducibility statement are present in the repository.

## Required before submission

### 1. Complete citation coverage

The 18-item reference list supports the conceptual Introduction, but the Methods and Results contain nearly all empirical claims without citations. Add primary or authoritative references for Reactome, gnomAD/LOEUF, HPA/GTEx, DepMap, GeneReviews, ClinVar, GWAS Catalog, the IgG glycome studies underlying the locus set, NG86, Ensembl, 1000 Genomes, and PopHuman. Cite the source studies behind the comparator-pathway disease assignments. This is the clearest current submission blocker.

### 2. Assemble the actual supplement and connect the figures

The manuscript says that full methods are in Supplementary Methods, but the repository currently contains modular methods notes rather than a single submission-ready supplement. Assemble those notes, add supplementary table identifiers, and cite every main figure/table from the Results. The local draft currently contains no figure or table callouts even though the Google Doc contains six figures.

### 3. Narrow two causal-sounding interpretations

- Replace the statement that comparator analysis "directly tests" and "demonstrates" topology dependence. The comparators are few, hand-curated, and unmatched; they provide a specificity check consistent with topology dependence.
- Recast the "Wald survivor-sampling bias" as a hypothesis rather than one of two mechanisms that "explain" the LOEUF inversion. The current analysis supports gene-length confounding; the recessive-survival account is biologically plausible but not independently tested.

### 4. Align the title and abstract with the measured contribution

The present title promises a direct demonstration of evolvability, while the study measures disease burden, cell-line essentiality, expression specificity, and assigned trait loci. A safer title would be:

> Layered disease burden, cell-line essentiality and glycan-trait associations across the N-glycosylation pathway

If “robustness and evolvability” remains in the title, the abstract should call it an interpretive model rather than the measured outcome.

### 5. Strengthen statistical reporting

For each primary contrast, report group sample sizes and an effect size with uncertainty, not only medians and p-values. State which analyses are primary versus exploratory, how multiple comparisons were handled, and whether the seven evidence streams were assessed under a formal integrated decision rule. The infinite IgG-locus odds ratio particularly needs its contingency-table counts and a confidence interval or an explicit note that the estimate is separation-limited.

### 6. Finish submission metadata

Remove working-draft metadata, choose the target journal, format references and sections to that journal, add data/code availability and author-contribution statements, and create a versioned archival release. Update the stale line describing the document as a first-pass draft.

## Strongest reviewer challenge

The most parsimonious alternative remains that shared early steps are broadly essential and specialized downstream enzymes simply control the assayed glycan phenotypes. The manuscript partly answers this with DepMap, IgG loci, and comparator pathways, but it does not directly measure evolvability as a system property. The paper survives this challenge if it presents the robustness/evolvability language as a model generated by the layered evidence, not as a demonstrated general principle.

## Readership assessment

This paper has a real but specialist readership: glycobiology, congenital disorders of glycosylation, human genetics, and network/evolutionary systems biology. Its most citable contribution is the integration of pathway position with disease burden, cell-line fitness, and glycan-trait association, plus the negative result that coding evolution does not follow the same gradient. It is unlikely to attract a broad audience on the pathway case study alone. A restrained title, a strong architecture figure, a reusable curated dataset, and a Discussion that clearly distinguishes observation from model would materially improve discoverability and citation potential.

## Submission gate

Do not start another broad analysis cycle. Complete the six items above, then run one final numerical/citation audit against the rendered journal-formatted manuscript. At that point the paper is ready to submit even if fine mapping, matched multi-pathway controls, and branch-model evolution remain future work.
