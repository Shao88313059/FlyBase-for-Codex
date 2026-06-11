# FlyBase-for-Codex
A Codex skill to use official FlyBase API and web pages. 一个教Codex如何用Flybase的Skill。 

功能
- 通过 FlyBase 官方 API 和网页核实基因、等位基因、品系、表型、表达、文献、GO 术语、直系同源等信息
- Checks genes, alleles, stocks, phenotypes, expression, publications, GO terms, orthologs, etc.
- 区分已验证事实与推测结论
- Distinguishes verified facts from uncertain interpretations
- 输出表格，包含状态、证据来源、FlyBase ID 和备注
- Returns a verification table with status, evidence, FlyBase ID, and notes

注意事项
- 默认只假设使用 Drosophila melanogaster
- Assumes _Drosophila melanogaster_ only as a fallback
- 不推断人类同源基因功能或疾病相关性
- Does not infer human ortholog function or disease relevance

参考/References
- https://flybase.github.io/api/swagger-ui/
- https://api.swaggerhub.com/apis/FlyBase/FlyBase/1.0
