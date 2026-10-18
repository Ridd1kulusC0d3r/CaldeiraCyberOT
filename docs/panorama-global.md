# 01 / Panorama global de cibersegurança OT

## Fronteira de pesquisa

O Caldeira acompanha **segurança de sistemas ciberfísicos**: automação industrial, energia, água e saneamento, petróleo e gás, transportes, saúde, edificações e manufatura. Não pressupõe que todos os segmentos usem a mesma arquitetura ou enfrentem o mesmo risco.

| Região | Fontes institucionais iniciais | Linha de pesquisa |
|---|---|---|
| **América do Norte** | [CISA](https://www.cisa.gov/resources-tools/resources/ics-recommended-practices) · [NIST](https://csrc.nist.gov/pubs/sp/800/82/r3/final) | Advisories, arquitetura e resposta |
| **Europa** | [ENISA](https://www.enisa.europa.eu/) · reguladores nacionais | Resiliência, cadeia de suprimentos e obrigações aplicáveis |
| **Ásia-Pacífico** | [ACSC Austrália](https://www.cyber.gov.au/publication/principles-of-operational-technology-cyber-security) | Princípios de proteção e segurança humana |
| **América Latina** | Autoridades nacionais, centros de resposta e reguladores setoriais | Exposição de ativos, maturidade e contexto local |
| **Global / transversal** | [ISA](https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards) · [MITRE](https://attack.mitre.org/matrices/ics/) | Controles, taxonomia e intercâmbio técnico |

**Atenção:** presença de uma fonte oficial não significa que seu documento seja vinculante em todas as jurisdições. A exigibilidade depende de país, setor, escopo e versão.

## Eixos de comparação

- **Setores:** energia elétrica, geração distribuída, petróleo/gás, manufatura, transportes, água, saúde e predial.
- **Pilha tecnológica:** sensores, atuadores, PLC/RTU, HMI, servidores SCADA, DCS, historiadores e gateways IIoT.
- **Superfície de risco:** integração TI/OT, conexões remotas de terceiros, protocolos legados, dispositivos sem suporte e mudanças não autorizadas.
- **Observabilidade:** inventário, fluxos, baseline operacional, telemetria passiva, alteração de configuração e trilhas de sessão.
- **Resiliência:** segmentação, segurança de processo, backup, restauração testada, governança e resposta conjunta TI/OT.

## Perguntas que um estudo global deve responder

1. Qual é a diferença entre incidente com **impacto real em OT** e incidente corporativo que afetou uma empresa industrial?
2. Como evoluiu a visibilidade operacional, **segundo qual método de medição**?
3. Que técnica MITRE ATT&CK for ICS foi **observada**, em qual evidência pública?
4. Como a arquitetura e a cadeia de suprimentos contribuíram para o risco?
5. Qual mitigação é tecnicamente válida **sem sacrificar safety, disponibilidade ou qualidade de processo**?

## Taxonomia mínima para catalogar casos

`case_id`, `data_incidente`, `data_publicacao`, `pais`, `setor`, `sistema`, `impacto_ot_confirmado`, `fonte_primaria`, `confidence`, `mitre_ics`, `mitigacoes`, `observacoes`.

Nunca atribua origem geográfica, agente ou impacto físico sem fonte que sustente a afirmação.

## Conceitos de arquitetura

~~~mermaid
flowchart TB
    IT["TI corporativa · serviços empresariais"]
    DMZ["DMZ industrial · serviços intermediários"]
    OPS["Operação · SCADA / HMI / historiador"]
    CTRL["Controle · PLC / RTU / DCS"]
    PHY["Processo físico · sensores e atuadores"]
    IT <-->|"fluxos permitidos e monitorados"| DMZ
    DMZ <-->|"conexões mínimas autorizadas"| OPS
    OPS <-->|"protocolos industriais"| CTRL
    CTRL <-->|"ação e medição"| PHY
~~~

**Esquema conceitual**, não topologia universal nem recomendação de regras específicas. Segmentar por riscos, zonas e conduítes, validar com operação e acompanhar a evolução de NIST e ISA/IEC 62443.

### Bibliografia fundamental
- [NIST Guide to OT Security](https://csrc.nist.gov/pubs/sp/800/82/r3/final)
- [ISA/IEC 62443](https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards)
- [ACSC Principles of OT Cyber Security](https://www.cyber.gov.au/publication/principles-of-operational-technology-cyber-security)
- [MITRE ATT&CK for ICS](https://attack.mitre.org/matrices/ics/)