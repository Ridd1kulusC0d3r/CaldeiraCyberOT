# Índice de relatórios e referências primárias OT

> Catálogo de **origens**, não espelho de PDFs. A curadoria privilegia páginas oficiais e análises dos investigadores que publicaram os achados. Data verificada: **2026-10-18**.

| Tema | Fonte / publicação | Uso na análise | Atenção |
|---|---|---|---|
| Normas e arquitetura | [NIST SP 800-82 Rev. 3 (2023, final)](https://csrc.nist.gov/pubs/sp/800/82/r3/final) | Baseline OT: confiabilidade, safety, arquitetura e controles | [Rev. 4 em draft, 2026](https://csrc.nist.gov/Projects/operational-technology-security/publications) |
| Contexto ATT&CK ICS | [Matriz ICS / MITRE](https://attack.mitre.org/matrices/ics/) | Táticas e técnicas com referências específicas | Técnica não comprova atribuição do ator |
| Arquitetura e detecção | [NSA/CISA — Know the Opponent (2022)](https://www.nsa.gov/Press-Room/Digital-Media-Center/Document-Gallery/igphoto/2003083007/) | Precursores e oportunidade de detecção | Documento orientativo |
| Estudos de incidentes | [INL — CyOTE Insights](https://cyote.inl.gov/tools/cyote-insights/) | Comparação de casos e relatórios precursores | Modelos e estimativas não são fatos medidos diretamente |
| SIS / TRITON | [Mandiant (2017)](https://cloud.google.com/blog/topics/threat-intelligence/attackers-deploy-new-ics-attack-framework-triton) | Investigação de malware para controladores de segurança | Separar intenção inferida de impacto observado |
| PIPEDREAM / INCONTROLLER | [Mandiant (2022)](https://cloud.google.com/blog/topics/threat-intelligence/incontroller-state-sponsored-ics-tool/) · [CISA AA22-103A](https://www.cisa.gov/news-events/cybersecurity-advisories/aa22-103a) | Capacidades e mitigação por produto | Não afirmar incidente industrial consumado |
| Industroyer2 | [ESET (2022)](https://www.welivesecurity.com/2022/04/12/industroyer2-industroyer-reloaded/) | Resposta e análise do incidente | Preservar diferença entre tentativa e impacto |
| FrostyGoop | [Dragos (2024)](https://hub.dragos.com/report/frostygoop-ics-malware-impacting-operational-technology) · [MITRE C0041](https://attack.mitre.org/campaigns/C0041/) | Campanha, Modbus e efeito operacional | Conclusões de atribuição dependem da fonte |
| Redes e PCAP | [Cyber4OT — paper SoftwareX (2025)](https://doi.org/10.1016/j.softx.2025.102196) · [repositório](https://github.com/krzysztof-cabaj/Cyber4OT) | Dataset experimental de tráfego | Experimento em testbed, não produção |
| Processo físico | [HAI](https://github.com/icsdataset/hai) · [SWaT/WADI iTrust](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/) · [BATADAL](https://www.batadal.net/data.html) | Pesquisa em anomalia física | Modalidades e termos de uso variam |
| Visibilidade de protocolos | [CISA ICSNPP](https://github.com/cisagov/ICSNPP) | Semântica e campos de rede observáveis | Parser não é prova de detecção pronta |
| Backup OT | [NIST SP 1339 (2026)](https://csrc.nist.gov/Projects/operational-technology-security/publications) | Recuperação e continuidade | Ver implementação real por setor |
| Acesso remoto em água | [NIST SP 1800-45 (2026)](https://csrc.nist.gov/Projects/operational-technology-security/publications) | Arquiteturas e decisão de acesso | Referência voluntária, não obrigação universal |

## Critério de uso e citação

Publicar **resumo original** com título, autoria, data do evento, data da publicação, URL de origem, tipo de evidência, limites e recomendação. Não confundir recomendações de fornecedor com conformidade normativa.

**Catálogos relacionados:** [Casos documentados](../docs/casos-ot/README.md) · [Datasets](../docs/datasets-ot.md) · [Método de CTI](../docs/metodologia-cti-ot.md).
