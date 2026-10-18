# Intelligence / Mapa de referência

O arquivo [attack_ics.json](attack_ics.json) contém IDs oficiais atuais, nomes e URLs. Não gera automaticamente atribuição, IOC, agente ou campanha com base em um único alerta.

## Perfis para estudo histórico

| Ator, campanha ou software | Tipo de entidade | Pergunta de CTI | Fonte primária de referência |
|---|---|---|---|
| **VOLTZITE** | nomenclatura de atividade de ameaça | Quais observáveis públicos permitem distinguir pré-posicionamento de comprometimento OT comprovado? | [Dragos Year in Review](https://www.dragos.com/ot-cybersecurity-year-in-review) |
| **ELECTRUM** | designação de grupo em relatórios especializados | Como os relatórios separam capacidades de interrupção e operação observada? | [Dragos](https://www.dragos.com/resources/) |
| **Sandworm** | grupo acompanhado por fontes diferentes, com sobreposição de nomenclaturas | Quais operações têm evidências públicas primárias? | [MITRE ATT&CK](https://attack.mitre.org/groups/G0034/) |
| **TEMP.Veles** | designação em pesquisa especializada | Que afirmações sobre o evento TRITON são documentadas? | [Mandiant TRITON](https://cloud.google.com/blog/topics/threat-intelligence/attackers-deploy-new-ics-attack-framework-triton) |
| **Industroyer2** | software documentado em ataque contra setor elétrico | Que capacidades foram analisadas versus efeitos demonstrados? | [MITRE S1072](https://attack.mitre.org/software/S1072/) |
| **TRITON / TRISIS** | software voltado a SIS | Quais informações sobre segurança de processo são públicas? | [MITRE S1009](https://attack.mitre.org/software/S1009/) |
| **PIPEDREAM / INCONTROLLER** | ferramenta analisada publicamente; não confundir descoberta com incidente | Qual a superfície tecnológica descrita? | [MITRE S1045](https://attack.mitre.org/software/S1045/) |
| **FrostyGoop** | software associado a caso OT documentado | Como distinguir alteração de parâmetros de impacto real? | [MITRE S1165](https://attack.mitre.org/software/S1165/) |

**Alerta de atribuição:** os rótulos usados por pesquisadores podem variar; aliases requerem comprovação em fontes, e correlação de nomes não prova identidade. Não atribuir um alerta sintético a esses grupos.

## Cuidado com o mapeamento

- `T0836`: **Modify Parameter**.
- `T0858`: **Change Operating Mode**, não sinônimo automático de denial of control (`T0813`).
- `T0843`: **Program Download**.
- `T0846`: **Remote System Discovery**; `T0842` é **Network Sniffing**.
- `T1692.001`: **Unauthorized Message: Command Message**. O ID antigo `T0855` redireciona à sub-técnica atual na edição consultada em 2026.

Referência mestre: [ATT&CK for ICS](https://attack.mitre.org/matrices/ics/) (revisão editorial 18/10/2026).