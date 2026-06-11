# FlyBase API Notes

These notes are intentionally concise. For exact schemas and endpoint parameters, check the official OpenAPI document at `https://api.swaggerhub.com/apis/FlyBase/FlyBase/1.0` or Swagger UI at `https://flybase.github.io/api/swagger-ui/`.

## Confirmed From Official API Documentation

- The API base URL is `https://api.flybase.org/api/v1.0/`.
- The OpenAPI document describes FlyBase API version `1.0`.
- Documented endpoint groups include species, sequence retrieval, GO ribbon data, updates, hitlists, gene summaries, datasets, Chado XML, protein domains, expression, and publications.
- Useful documented GET paths include:
  - `/species/lookup/{flybaseIds}` for genus, species, and abbreviation for comma-delimited FlyBase IDs.
  - `/sequence/region/{species}/{location}` and `/sequence/id/{flybaseId}` for sequence retrieval.
  - `/sequence/id/{flybaseId}/{subType}` for subtype sequence retrieval; documented subtypes include `FBgn`, `FBtr`, `FBpp`, `FBcl`, `FBsf`, `FBti`, `FBtp`, `exon`, `intron`, `five_prime_utr`, `three_prime_utr`, and `CDS`.
  - `/ribbon/go/{goDomain}/{fbgnId}` for GO slim/ribbon data; documented domains are `biological_process`, `cellular_component`, and `molecular_function`.
  - `/updates/{flybaseId}` for recent update information.
  - `/hitlist/fetch/{flybaseIds}` for HitList information.
  - `/gene/summaries/auto/{fbgnId}` for automatically generated gene summaries.
  - `/downloads/FBlc/associated_data/{fblcId}` for dataset-associated strains, cell lines, and features.
  - `/chadoxml/{flyBaseId}` for ChadoXML by current valid FlyBase ID.
  - `/domain/{flyBaseGeneId}` and `/domain/{flyBasePolypeptideId}` for protein domains. The OpenAPI document lists these as separate operations with the same path pattern, so verify behavior with the actual ID type.
  - `/expression/proteome/{flyBaseGeneId}` for proteomic LFQ expression values and developmental stages.
  - `/fbrf/{flyBaseReferenceId}/abstract` for publication abstracts when available.
  - `/fbrf/filter` as a POST endpoint for filtering FBrf IDs by query term.

Because endpoint details can change, always re-check the OpenAPI document before relying on an exact path in a publication, script, or large batch.

## Identifier Prefix Hints

- `FBgn`: gene
- `FBal`: allele
- `FBst`: stock
- `FBpp`: polypeptide/protein product
- `FBtr`: transcript
- `FBbt`: anatomy/development controlled vocabulary term
- `FBcv`: controlled vocabulary term
- `FBti`: transposable element insertion
- `FBsf`: sequence feature

These prefix meanings are practical FlyBase conventions. If a task depends on exact object type, verify by resolving the ID through FlyBase.

## Recommended Claim-To-Source Mapping

| Claim type | First source to try | Cross-check when needed |
|---|---|---|
| Gene identity, symbol, full name, synonyms | Gene summaries API or FlyBase report page | FlyBase report page history/secondary IDs |
| GO molecular function/process/component | GO ribbon API or FlyBase GO section | Linked GO evidence/publication |
| Expression pattern, tissue, stage | Expression API or FlyBase expression section | Linked assay/publication |
| Transcript/protein/sequence | Sequence API | FlyBase transcript/protein report page |
| Protein domains | Domains API | InterPro/Pfam links from FlyBase when present |
| Publications | Publications API or FlyBase references | PubMed/DOI record |
| Dataset membership | Datasets API | Dataset landing page or publication |
| Recently changed records | Updates API | FlyBase report page current state |

## Batch Verification Guidance

For large gene lists:

1. Keep the original input column.
2. Add stable ID, current symbol, organism, status, source endpoint, source date, and notes columns.
3. Cache raw API responses when allowed by the project workflow.
4. Flag ambiguous symbols and all failed lookups for manual review.
5. Never silently drop unmatched records.

## Failure Labels

- `not verified - network`: could not reach FlyBase/API.
- `not verified - endpoint`: endpoint path or parameters were not confirmed.
- `not verified - no match`: query succeeded but returned no matching record.
- `ambiguous`: multiple plausible records or species; user/context must disambiguate.
- `contradicted`: official evidence conflicts with the claim.
