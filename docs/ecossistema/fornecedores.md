# 02 / Fornecedores de segurança OT

> Curadoria de capacidades publicamente documentadas. **Não é ranking**, recomendação de compra, avaliação independente de eficácia nem indicação de liderança comercial.

| Empresa | Foco em OT/ICS | Casos de estudo | Fonte oficial |
|---|---|---|---|
| **[Nozomi Networks](https://www.nozominetworks.com/)** | Descoberta e inventário de ativos, monitoramento de rede, análise de protocolos e detecção de anomalias. | Observabilidade de comunicação OT e inventário | [Site institucional](https://www.nozominetworks.com/) |
| **[Claroty](https://claroty.com/)** | Segurança de CPS/XIoT, visibilidade e gestão de exposição em contextos industriais e outros ambientes ciberfísicos. | Governança de ativos e risco | [Site institucional](https://claroty.com/) |
| **[Dragos](https://www.dragos.com/)** | Threat intelligence industrial, detecção de ameaças ICS, análise de incidentes e serviços especializados. | Adversários, incidentes e detecções | [2026 Year in Review](https://www.dragos.com/ot-cybersecurity-year-in-review) |
| **[Fortinet](https://www.fortinet.com/solutions/ot-security)** | Segurança de redes IT/OT, segmentação, dispositivos industriais robustecidos, acesso seguro e integrações de SecOps. | Controles de comunicação entre zonas | [OT Security](https://www.fortinet.com/solutions/ot-security) |
| **[Tenable OT](https://www.tenable.com/products/ot-security)** | Inventário, avaliação de exposição, visibilidade de dispositivos industriais e priorização de riscos. | Gestão contextual de exposição | [Tenable OT Security](https://www.tenable.com/products/ot-security) |

## Como avaliar fornecedores sem transformar pesquisa em publicidade

| Critério | Pergunta |
|---|---|
| **Cobertura** | Quais ativos, protocolos e versões de firmware são identificáveis? |
| **Modo de coleta** | Passivo, ativo, híbrido? Quais são os impactos de cada método? |
| **Safety** | Como o fabricante documenta riscos operacionais, janelas de manutenção e testes de compatibilidade? |
| **Integração** | Há conectores SIEM, SOAR, APIs, SBOM, inventário e modelos de dados exportáveis? |
| **Detecção** | Existem regras explicáveis, contexto ATT&CK for ICS, falsos positivos mensuráveis e procedimentos de tuning? |
| **Exposição** | A priorização considera criticidade de processo e compensações disponíveis? |
| **Dependência** | Há limitações de licença, nuvem, retenção de tráfego, alta disponibilidade e requisitos de conectividade? |
| **Evidência** | A afirmação vem de documentação pública, estudo independente, teste reproduzível ou material comercial? |

### Nota sobre descoberta ativa

**Não presumir que consulta ativa ou varredura convencional seja segura em todos os PLCs/RTUs.** Testar primeiro em ambiente segregado e com aprovação da engenharia e da operação. Comparar produtos com critérios objetivos e não apenas descrições promocionais.

### Referência de mercado (não classificação)

A seleção de cinco fornecedores apresentada no pedido original foi aproveitada por pertinência ao estudo. Não há base metodológica nesta curadoria para declará-los os cinco maiores, nem para ordenar sua liderança global. Estudos de mercado devem explicitar data, método de amostragem, patrocinador e universo avaliado.

### Outras categorias a pesquisar

Integradores OT; automação e engenharia; fornecedores de SIS/DCS; proteção de endpoints compatíveis com OT; soluções de acesso remoto para manutenção; sistemas de inventário; ferramentas de análise de pacotes industriais.