---
name: flybase-for-codex
description: Verify Drosophila/FlyBase biological information with evidence-first workflows using the official FlyBase API and FlyBase web pages. Use this skill to deal with fruit fly/Drosophila related requests, e.g. searching or validating fruit fly genes, alleles, stocks, phenotypes, expression, publications, GO terms, orthologs, datasets, sequences, or any claim involving FlyBase IDs such as FBgn, FBal, FBst, FBpp, FBtr, FBbt, FBcv, FBti, FBsf, or gene symbols.
---

# FlyBase for Codex

Use this skill to verify fruit fly information without treating guesses as facts. Prefer official FlyBase API evidence, then official FlyBase pages, then literature databases. Always separate confirmed facts from uncertain interpretations.

## Core Rule

Do not answer from memory when a claim can be checked. Verify against a source and cite the endpoint/page used. If network access, API access, or an identifier lookup fails, say `not verified` and explain what was attempted.

## Official Sources

- API docs: `https://flybase.github.io/api/swagger-ui/`
- OpenAPI JSON: `https://api.swaggerhub.com/apis/FlyBase/FlyBase/1.0`
- Base API URL from the OpenAPI spec: `https://api.flybase.org/api/v1.0/`
- FlyBase gene pages normally use stable IDs, for example `https://flybase.org/reports/FBgn0000008`

Read `references/api-notes.md` before doing endpoint-heavy work or when unsure which endpoint to use.

## Verification Workflow

1. Normalize the query.
   - Preserve the user's exact symbol/name.
   - Identify organism if provided. Default to `Drosophila melanogaster` only as an assumption, and label it as such.
   - Identify known FlyBase IDs and their prefixes.

2. Resolve identifiers before checking facts.
   - Prefer stable FlyBase IDs over symbols because symbols can be aliases or reused.
   - If multiple records match a symbol, report ambiguity and verify only after selecting the correct record.
   - For gene claims, look for a current `FBgn` and synonyms/secondary IDs.

3. Verify each claim independently.
   - Gene identity/name/synonyms: gene summary or report evidence.
   - Molecular function/process/component: GO ribbon or annotations.
   - Expression/anatomy/stage: expression endpoint/page evidence.
   - Sequence/transcript/protein: sequence endpoint and returned identifiers.
   - Alleles/phenotypes/stocks: relevant FlyBase report pages or API endpoints when available.
   - Publications: publication endpoint/page and PMID/DOI when available.

4. Cross-check high-impact or surprising claims.
   - Use at least two official FlyBase views or one FlyBase source plus the linked paper.
   - Treat orthology, phenotype causality, and expression specificity as interpretation unless the source directly supports it.

5. Return a verification table.
   - `claim`: the exact claim being checked.
   - `status`: `verified`, `partially verified`, `contradicted`, or `not verified`.
   - `evidence`: endpoint/page and key returned fields, paraphrased.
   - `identifier`: stable FlyBase ID(s).
   - `notes`: ambiguity, assumptions, date checked, or follow-up needed.

## API Use

Use `scripts/flybase_api.py` for quick endpoint checks when Python and network access are available. Examples below are copied from the official OpenAPI paths:

```bash
python scripts/flybase_api.py get /species/lookup/FBgn0000490
python scripts/flybase_api.py get /gene/summaries/auto/FBgn0000490
python scripts/flybase_api.py raw /sequence/id/FBgn0000490
```

If the exact endpoint path is uncertain, open the OpenAPI JSON or Swagger UI first. Do not invent endpoint paths; say the endpoint is unknown until confirmed.

## Evidence Standards

- Prefer stable identifiers and exact API fields over prose snippets.
- Quote sparingly; paraphrase source content and include URL/endpoint.
- Record the date of verification when the user is building a dataset or manuscript.
- Distinguish `no result found` from `API unavailable` and from `endpoint not confirmed`.
- Do not infer human ortholog function, disease relevance, or pathway role from a Drosophila gene page unless an official orthology/annotation source directly supports it.

## Output Template

```markdown
Checked on: YYYY-MM-DD

| Claim | Status | Evidence | FlyBase ID | Notes |
|---|---|---|---|---|
| ... | verified / partially verified / contradicted / not verified | Official endpoint/page and returned field summary | FBgn... | ... |

Unverified or ambiguous items:
- ...
```
