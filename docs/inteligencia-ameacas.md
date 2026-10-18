# 03 / Inteligência de ameaças aplicada à OT

## Modelo de análise do Caldeira

**Fato relatado → evidência verificável → ativo e contexto → comportamento ATT&CK for ICS → consequência operacional → mitigação viável.**

Uma campanha direcionada a uma empresa industrial **não prova**, por si só, comprometimento de PLCs, alteração de processo ou intenção de sabotagem. O campo `impacto_ot_confirmado` deve ser independente da classificação `vítima_industrial`.

| Nível de evidência | Definição |
|---|---|
| **A · Primária** | Advisory oficial, relatório de resposta, telemetria/caso técnico verificável |
| **B · Corroborada** | Fontes independentes concordantes, com referências ao material primário |
| **C · Relato indireto** | Imprensa ou vendor summary sem documentação técnica suficiente |
| **D · Hipótese** | Suposição analítica explicitamente identificada, sem comprovação |

## Ficha de análise

~~~yaml
id: CAL-OT-CASE-0001
titulo: "Exemplo fictício de investigação defensiva"
status: "simulacao"
data_evento: null
data_publicacao: "2026-10-18"
setor: "manufatura"
regiao: "ficticia"
ativos: ["HMI", "PLC"]
impacto_ot_confirmado: false
evidencia: []
mitre_attack_ics: []
confidence: "nao_aplicavel"
hipotese: "anomalia de comunicação a investigar"
decisao_defensiva: "validar baseline com engenharia"
~~~

## Fontes a cruzar

- [MITRE ATT&CK for ICS](https://attack.mitre.org/matrices/ics/), incluindo relação entre técnica, grupo e software quando documentada.
- [Dragos 2026 Year in Review](https://www.dragos.com/ot-cybersecurity-year-in-review): análise de adversários e tendências da empresa.
- [CISA ICS Recommended Practices](https://www.cisa.gov/resources-tools/resources/ics-recommended-practices): fundamentos defensivos e resposta.
- [NIST SP 800-82 Rev. 3](https://csrc.nist.gov/pubs/sp/800/82/r3/final): controles e arquitetura.

## Temas para investigação

1. Invisibilidade de ativos, fluxos e alterações de configuração.
2. Exposição e governança de acessos remotos de integradores.
3. Ransomware e dependências entre serviços TI e operação industrial.
4. Monitoramento de engenharia, HMI e sistemas de gestão de processo.
5. Segurança de terceiros, supply chain, vulnerabilidades e gestão de mudanças.
6. Resposta conjunta entre segurança digital, operação e segurança de processo.

**Limites de uso:** estudar comportamentos e defesas em ambientes didáticos próprios; não extrapolar casos simulados para técnicas observadas em incidentes reais.