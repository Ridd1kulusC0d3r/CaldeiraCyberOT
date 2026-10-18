# 04 / Normas, autoridades e formação para Cyber OT

> **REFERENCE AUTHORITY MAP** · Revisado em 18/10/2026. Distinguir mantenedor normativo, agência governamental, instituto de treinamento e base técnica. [Leia o guia de referenciais com análise](../referenciais-ot.md).

| Instituição | Tipo | Contribuição para OT/ICS | Fonte primária |
|---|---|---|---|
| **ISA / IEC** | Organismos de normalização e comitês técnicos | Família **ISA/IEC 62443**, segurança de sistemas de automação e controle | [Série ISA/IEC 62443](https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards) |
| **ISA / ISA-95** | Trabalho normativo sobre integração empresa e controle | Modelagem de funções empresariais e industriais, com uso do modelo Purdue como referência | [Comitê ISA-95](https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa95) |
| **MITRE** | Organização de pesquisa; base de conhecimento | ATT&CK for ICS, táticas e técnicas do comportamento adversário | [Matriz ICS](https://attack.mitre.org/matrices/ics/) |
| **NIST (EUA)** | Instituto nacional de padrões e tecnologia | Guia **SP 800-82 Rev. 3**, com segurança, desempenho e confiabilidade de OT | [Guia oficial](https://csrc.nist.gov/pubs/sp/800/82/r3/final) |
| **CISA (EUA)** | Agência governamental de infraestrutura e cibersegurança | Advisories ICS, mitigação de riscos e orientações de resiliência | [Mitigações OT de 2025](https://www.cisa.gov/resources-tools/resources/primary-mitigations-reduce-cyber-threats-operational-technology) |
| **SANS Institute / SANS ICS** | Formação técnica privada / pesquisa educacional | Cursos de ICS, certificações relacionadas e **Five ICS Critical Controls** | [SANS ICS](https://www.sans.org/cybersecurity-focus-areas/industrial-control-systems-security) |
| **ACSC / ASD (Austrália)** | Centro governamental de cibersegurança | Princípios de segurança em OT | [Princípios OT](https://www.cyber.gov.au/publication/principles-of-operational-technology-cyber-security) |
| **ENISA (União Europeia)** | Agência de cibersegurança da UE | Resiliência e orientações para infraestrutura e setores essenciais | [ENISA](https://www.enisa.europa.eu/) |

## Referências que não devem ser confundidas

- **ISA/IEC 62443 é uma série de normas**, com famílias gerais, políticas/procedimentos, sistema e componentes; citar a **parte e edição**. Não é uma lei mundial única.
- **ISA-95 não é sinônimo do modelo Purdue.** Usa o Purdue Reference Model for CIM como base para integração entre funções de empresa e produção.
- **MITRE ATT&CK for ICS** não é norma nem catálogo de controles obrigatórios: descreve comportamentos adversários e fornece taxonomia para estudar detecção.
- **NIST SP 800-82** é guia técnico, não certificação de conformidade.
- **CISA** publica documentos relevantes internacionalmente, mas a aplicabilidade legal depende de jurisdição, setor e obrigação.
- **SANS** é referência de capacitação profissional e pesquisa educacional especializada; evitar classificá-la como agência reguladora ou “maior referência acadêmica mundial”, expressão sem critério demonstrado.

## Atualidade e aplicação

**NIST SP 800-82 Rev. 3** é a edição final de **setembro de 2023**. Em outubro de 2026 há **draft inicial da Rev. 4** (ver planejamento publicado na [página NIST](https://csrc.nist.gov/pubs/sp/800/82/r3/final)). Não tratar draft como publicação final.

A série **ISA/IEC 62443** contém múltiplas partes com atualizações independentes. A **aplicabilidade regulatória** de cada requisito varia por país, setor e contrato.

## Guia CISA 2025 em cinco tópicos

A ficha [Primary Mitigations](../guias/cisa-mitigacoes-ot.md), publicada em **06/05/2025** por CISA, FBI, EPA e DOE, prioriza redução de exposição OT pública, credenciais padrão, acesso remoto, segmentação IT/OT e preparação de operação manual segura. Veja o **guia de estudo independente** com perguntas de auditoria e limites operacionais.

## Referências SANS ICS adicionais

- [Five ICS Cybersecurity Critical Controls](https://www.sans.org/white-papers/five-ics-cybersecurity-critical-controls): resposta a incidentes, arquitetura defensável, visibilidade, acesso remoto e vulnerabilidades com base em risco.
- [Cursos e trilhas SANS ICS](https://www.sans.org/cybersecurity-focus-areas/industrial-control-systems-security).

## Como catalogar uma nova jurisdição

Registrar **autoridade, documento, edição/ano, validade legal, setores aplicáveis, requisitos de notificação, responsáveis e fonte primária**. Não presumir universalidade. O Caldeira é um hub global de estudo, não consultoria de conformidade.

**Navegação:** [referenciais fundamentais](../referenciais-ot.md) · [fornecedores](fornecedores.md) · [biblioteca de relatórios](../../relatorios/README.md).
