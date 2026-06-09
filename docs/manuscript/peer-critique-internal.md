# Internal Peer Critique — N-Glycosylation Manuscript Draft

Date: 2026-06-09  
Source: Self-generated savage critique before external submission  
Purpose: Identify the weakest points and plan revisions

---

## Summary Verdict

The paper's positive evidence reduces to: *CDG diseases come from disrupting shared early steps, and downstream genes have more GWAS hits in trait categories relevant to their known biology.* This is confirmatory of textbook glycobiology. The robustness/evolvability framing promises theoretical contribution to evolutionary systems biology that the data do not yet support.

---

## Critique by Category

### I. The Central Claim Is Nearly Unfalsifiable

The model predicts upstream = robust, downstream = evolvable. When constraint analysis contradicts this (upstream genes have higher LOEUF = less constrained), the paper reframes as "robustness is distributed." When pop-gen finds no gradient, this becomes "evolvability operates through non-coding channels." When conservation finds no gradient, this "confirms" regulatory evolvability.

Every result either confirms the model or is explained away as consistent with a more nuanced version. A framework that cannot be falsified is not a scientific argument.

**Fix needed:** State explicitly what would falsify the model. Pre-register a directional prediction before further analysis.

---

### II. The Primary Positive Finding Is a Tautology

Disease burden concentrates in the upstream core — trivially true because shared essential steps affect all glycoproteins when disrupted. Specialized downstream steps affect subsets. This is in every glycobiology textbook.

**Missing null model:** Would any pathway show the same disease architecture when classified as "shared core steps" vs. "specialized downstream steps"? Almost certainly yes. The finding may not be specific to N-glycosylation's evolutionary architecture.

**Fix needed:** Test the null. Take a matched set of other biosynthetic pathways and classify their genes the same way. If the disease gradient is universal, N-glyco is not a special case study.

---

### III. "Evolvability" Is Never Measured

The paper uses "evolvability" (Kitano/Wagner/Payne sense: capacity to generate heritable phenotypic variation) but measures:
- Absence of CDG disease → not evolvability, just complement of severe constraint
- GWAS association counts → standing variation that has been tolerated, not capacity to generate adaptive variation
- FST/iHS → found nothing

**Fix needed:** Either (a) replace "evolvability" with a more accurate term throughout ("trait diversity," "interface biology," "phenotypic tolerance"), or (b) actually measure evolvability — e.g., using dN/dS branch tests, McDonald-Kreitman, or glycan phenotype variance data across populations.

---

### IV. The LOEUF Inversion Is Unexplained and Interesting

Upstream-core genes have higher LOEUF (median 0.91) than downstream (0.74), meaning upstream is *less* constrained. This directly contradicts the hypothesis. The Discussion response ("robustness is distributed, not upstream-concentrated") is circular — it says the most constrained genes are constrained for biological reasons, which is vacuous.

The LOEUF inversion may be the paper's **most genuinely interesting result** and deserves a real explanation.

**Fix needed:** Test whether paralog count, expression breadth, or network centrality explains the LOEUF direction. Run a regression of LOEUF on pathway group + paralog count + expression breadth. This is a specific, testable claim that would either explain the inversion or make it more mysterious — either outcome is interesting.

---

### V. The GWAS Evidence Is Essentially Meaningless as Architecture Evidence

- "Nearly every pathway gene had at least one association" — true of any 101 human genes
- Terminal-modification enzymes (sialyltransferases, fucosyltransferases) have immune GWAS hits because they *are* immune enzymes — not because of downstream architecture
- Category profiles are derived from the same contaminated counts; no genome-wide matched null was used

**Fix needed:** Compare downstream category profile to a genome-wide matched null (same gene length, expression breadth, tissue specificity). If the enrichment holds, it's real. If not, it's noise.

---

### VI. Results Section Describes Inputs as Outputs

Paragraphs in Results describe what was *assigned* (catastrophic-potential priors, interface-layer priors) as if these were *discovered*. This conflates model inputs with model outputs.

**Fix needed:** Move assigned priors/features back to Methods. Results should report only what was discovered from external data.

---

### VII. The Comparator Pathway Analysis Is Confounded

- Heme is uniformly constrained because heme is essential for all cells (every step matters), not because it lacks a "combinatorial output layer"
- CoQ is uniformly tolerant partly due to dietary supplementation and redundancy — nothing to do with topology
- Two comparators are too few and are not matched on expression breadth, essentiality, or tissue specificity

**Fix needed:** Either properly control the comparison (match on expression breadth, tissue ubiquity) or hedge the comparator section down to a "preliminary observation." As written, it overreaches.

---

### VIII. The Discussion Restates Rather Than Synthesizes

Nearly every Discussion paragraph: restate result → "consistent with" hypothesis → hedge. This is not synthesis. The Discussion should raise alternative explanations, test them against data, and reach a conclusion.

**Fix needed:** For each Discussion subsection, add: (1) the strongest alternative explanation for the result, (2) why the data favor the architecture interpretation over the alternative, (3) what specific follow-up would distinguish them.

---

### IX. Too Many Null Results Stacked Together

- Constraint: wrong direction
- Conservation: null
- Population genetics: null
- Comparators: confounded

Positive evidence = disease architecture gradient (upstream severe, downstream trait-rich). The paper should be honest: this single evidence stream is the paper's contribution. Everything else is context.

**Fix needed:** Restructure around the disease architecture finding as the primary result. Reframe constraint, conservation, and pop-gen as "what we checked and why the nulls are informative" rather than treating them as co-equal evidence streams.

---

### X. Writing Is Defensively Hedged to Self-Refutation

The Limitations section renders most of the analysis unreportable:
- "constraint results should not be cited as evidence of a demonstrated constraint gradient"
- "population-genetic results should be treated strictly as exploratory context"

After seven major limitations, what is demonstrated? The hedging strategy backfires: if nothing is claimed, nothing is contributed.

The Introduction compounds this: *"If the evidence is mixed, the result is still informative."* This pre-emptive escape hatch before any data are shown signals the authors don't believe the hypothesis.

**Fix needed:** Cut Limitations to the three most important. Be specific about what IS demonstrated, not just what isn't.

---

### XI. The Title and Framing Overpromise

"Robustness and evolvability across a glycosylation pathway" promises theoretical contribution to evolutionary systems biology. The paper demonstrates a disease severity gradient. These are different things.

A more accurate title would be something like: *"Disease architecture and glycan-output trait associations are layered across the N-glycosylation pathway"*

---

## What Would Save This Paper

| Problem | Fix |
|---------|-----|
| Unfalsifiable central claim | State what would falsify it; identify pre-registered directional predictions |
| Disease gradient is a tautology | Test null model across other pathways |
| "Evolvability" unmeasured | Replace with accurate term OR measure it (dN/dS, glycan variance, MK test) |
| LOEUF inversion unexplained | Regression: LOEUF ~ pathway_group + paralog_count + expression_breadth |
| GWAS evidence has no null | Match against genome-wide null by gene length + expression breadth |
| Results describes inputs | Move priors to Methods |
| Comparator analysis confounded | Match or heavily hedge |
| Discussion restates results | Add: alternative explanation → why data favor architecture interpretation → falsifying follow-up |
| Too many nulls presented equally | Restructure: disease architecture = primary; nulls = informative context |
| Over-hedged limitations | Cut to 3; be specific about what IS shown |
| Title overpromises | Retitle to match actual contribution |

---

## Bottom Line

The paper currently has one clean finding (disease architecture gradient) wrapped in a theoretical framework it cannot support, surrounded by null results it presents as confirmatory. The path forward is either:

**Option A (conservative):** Strip the robustness/evolvability framing down to "disease architecture and trait associations are layered." Make the disease gradient the paper. Add the LOEUF inversion as a genuinely interesting secondary finding. Accept that this is a careful observation paper, not a theory paper.

**Option B (ambitious):** Earn the robustness/evolvability framing by actually measuring evolvability. Use glycan phenotype variance data (e.g., Lauc group IgG glycome GWAS), branch-specific dN/dS tests, or expression variance decomposition to demonstrate that downstream genes generate more heritable phenotypic variation. This would make the paper what its title claims.
