# Referências fundamentais de cibersegurança OT

> **CALDEIRA / REFERENCE INTELLIGENCE** · revisão editorial: 18/10/2026 · objetivo: ensino, comparação e investigação defensiva global. Este guia não substitui avaliação de engenharia, safety, consultoria jurídica ou normas adquiridas com licença.

**Pergunta que organiza o material:** estamos falando de um requisito, uma representação arquitetural, uma técnica adversária, uma recomendação governamental ou uma funcionalidade de produto? São categorias distintas.

## Visão executiva: seis tipos de referência

| Categoria | Referência | O que responde | O que **não** demonstra |
|---|---|---|---|
| **Normas de segurança de IACS** | [ISA/IEC 62443](https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards) | O que requerem as partes aplicáveis para gestão de risco, sistema e componentes industriais? | Não é lei única, nem garante certificação de toda a planta. |
| **Integração e arquitetura funcional** | [ISA-95](https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa95) e modelo Purdue de referência | Quais funções e trocas entre operações e empresa precisam ser entendidas? | A numeração não é, sozinha, uma regra de firewall nem um requisito de conformidade. |
| **Taxonomia de adversários** | [MITRE ATT&CK for ICS](https://attack.mitre.org/matrices/ics/) | Quais táticas e técnicas são documentadas? Quais lacunas de visibilidade existem? | Uma técnica associada a alerta sintético não prova ataque real ou autoria. |
| **Guia de segurança** | [NIST SP 800-82 Rev. 3](https://csrc.nist.gov/pubs/sp/800/82/r3/final) | Como proteger OT considerando confiabilidade, desempenho e segurança física? | Guia não equivale automaticamente a exigência legal global. |
| **Recomendações para exposição e resiliência** | [CISA: Primary Mitigations (2025)](guias/cisa-mitigacoes-ot.md) | Quais medidas básicas priorizar para ativos OT expostos ou conectividade remota? | Recomendação setorial não é ordem para desconectar sistemas de produção sem planejamento. |
| **Treinamento e priorização** | [SANS ICS](https://www.sans.org/cybersecurity-focus-areas/industrial-control-systems-security) | Como estruturar aprendizagem, detecção, resposta e controles fundamentais? | Fornecedor de treinamento não é autoridade regulatória ou entidade acadêmica governamental. |

### O que muda em OT

O NIST destaca requisitos de **desempenho, confiabilidade e safety**. Em consequência, alterações de segmentação, políticas, descoberta ativa, proteção de endpoint ou resposta automática precisam considerar engenharia de processo, janelas de manutenção, compatibilidade com legado e procedimentos de segurança. Não existe promessa universal de “segurança sem risco de parada”. Fonte: [NIST SP 800-82r3](https://csrc.nist.gov/pubs/sp/800/82/r3/final).

## ISA/IEC 62443: quatro famílias, múltiplas partes

| Família | Assunto | Pergunta operacional |
|---|---|---|
| **62443-1-x** | General: termos, conceitos, modelos | Quais definições e conceitos descrevem o ambiente? |
| **62443-2-x** | Policies & Procedures: programa, operação, provedores | Quais papéis, procedimentos e práticas de gestão se aplicam? |
| **62443-3-x** | System: análise de risco e requisitos do sistema | Como analisar risco e definir requisitos para zonas e conduítes? |
| **62443-4-x** | Component: desenvolvimento seguro e requisitos de componentes | Que requisitos são relevantes para produtos e componentes? |

O número da **parte** e a **edição vigente** devem acompanhar qualquer citação; a família não é um único documento. A ISA apresenta responsabilidades distribuídas entre proprietários, fornecedores, integradores e prestadores de serviços. Fonte: [ISA — série oficial](https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards). Documentos normativos integrais devem ser consultados por acesso autorizado, não copiados neste projeto.

## Modelo Purdue e ISA-95 não são sinônimos

A [ISA-95](https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa95) define integração entre funções de controle/manufatura e sistemas empresariais, usando como base o **Purdue Reference Model for CIM**. O contexto inicial central está na interface entre **níveis 3 e 4**.

- O Purdue é uma **abstração funcional clássica**, não um mapa obrigatório para qualquer fábrica.
- **L3.5 (DMZ industrial)** é uma convenção de projeto amplamente empregada, não um nível universal do modelo original.
- **L5 / conectividade externa**, quando representado neste repo, é uma extensão didática adotada em materiais e arquiteturas de referência, não uma declaração de que a ISA-95 impõe seis níveis obrigatórios.
- Zonas, conduítes, identidades e fluxos reais devem ser derivados do processo industrial, de riscos e das políticas aplicáveis.

![Visão didática da hierarquia Purdue](../assets/brand/purdue-layers.svg)

## ATT&CK for ICS: como aplicar sem distorção

A [matriz ICS](https://attack.mitre.org/matrices/ics/) descreve **táticas e técnicas de adversários**. Uma técnica associada à hipótese de detecção requer evidência do comportamento, não apenas o nome do protocolo. O núcleo de eventos fictícios do Caldeira permite formular hipóteses, mas **não demonstra comprometimento industrial**.

[Consulte o catálogo MITRE revisado](../core/intel/README.md) e a [metodologia de proveniência](metodologia-cti-ot.md).

## NIST SP 800-82: versões

A [revisão 3 de 2023](https://csrc.nist.gov/pubs/sp/800/82/r3/final) é a referência final nesta curadoria (18/10/2026). O NIST informa um **rascunho inicial da revisão 4 (2026)**; não confundir *draft* com documento final. Consulte o histórico na página oficial antes de alterar recomendações.

## CISA: guia prático prioritário

[CISA / FBI / EPA / DOE, maio de 2025](guias/cisa-mitigacoes-ot.md) relaciona cinco grupos de mitigação:

1. Redução da exposição OT à internet.
2. Remoção de credenciais padrão e uso de credenciais fortes e únicas.
3. Proteção do acesso remoto com autenticação e privilégios limitados.
4. Segmentação IT/OT e DMZ apropriada.
5. Preparação e ensaio da capacidade de operação manual segura.

As cinco são recomendações das agências; a interpretação e o plano de adoção precisam da equipe responsável pelos processos físicos.

## SANS ICS: da teoria à habilidade

[SANS ICS Security](https://www.sans.org/cybersecurity-focus-areas/industrial-control-systems-security) oferece formação técnica especializada. Seus [Five ICS Cybersecurity Critical Controls](https://www.sans.org/white-papers/five-ics-cybersecurity-critical-controls) priorizam **ICS incident response; defensible architecture; network visibility and monitoring; secure remote access; risk-based vulnerability management**.

Eles não substituem a norma ISA/IEC 62443 e não fornecem certificação de conformidade para uma planta inteira.

## Como usar na prática do Caldeira

| Projeto | Uso correto | Saída de estudo |
|---|---|---|
| [CAL-LAB-001](../cases/README.md) | Regra sintética para evento de escrita Modbus fora de baseline | Hipótese defensiva + evidência SHA-256 |
| [CAL-LAB-002](../cases/README.md) | Identificar fluxo IT→OT fictício não previsto na matriz de zonas | Caso sobre governança de fluxos; **não** comprova pivô |
| [Atlas OT](casos-ot/README.md) | Verificar se um evento público tem impacto operacional sustentado | Ficha histórica com grau de confiança |
| [Biblioteca](../relatorios/README.md) | Ler achados de fornecedores com metodologia e amostra | Análise original e ressalvas |

**Complemento:** [fornecedores e capacidades](ecossistema/fornecedores.md) · [avaliação técnica neutra](ecossistema/avaliacao-fornecedores.md) · [instituições](ecossistema/instituicoes.md).

## Referências primárias

- ISA: https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards
- ISA-95: https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa95
- MITRE: https://attack.mitre.org/matrices/ics/
- NIST: https://csrc.nist.gov/pubs/sp/800/82/r3/final
- CISA: https://www.cisa.gov/resources-tools/resources/primary-mitigations-reduce-cyber-threats-operational-technology
- SANS: https://www.sans.org/white-papers/five-ics-cybersecurity-critical-controls

**Nota editorial:** fontes comerciais e vídeos são úteis como ponto de entrada, mas este guia prioriza documentos dos autores e mantenedores dos referenciais.
