# 08 / Metodologia de inteligência OT orientada por evidências

## Da fonte à decisão operacional

~~~mermaid
flowchart LR
  A["Fonte primária / aviso / relatório"] --> B["Proveniência, data e versão"]
  B --> C["Fato, inferência ou hipótese?"]
  C --> D["Ativos, setor, processo e impacto"]
  D --> E["Comportamento MITRE ATT&CK ICS"]
  E --> F["Cobertura de telemetria e controles"]
  F --> G["Recomendação revisada por OT e safety"]
  G -. "nova evidência" .-> B
~~~

A missão do Caldeira é **normalizar, correlacionar e contextualizar evidências**. O repositório não gera scripts de intrusão e não orquestra o Mininet. Isso pertence ao projeto [mininet](https://github.com/Ridd1kulusC0d3r/mininet), mantido separadamente.

## Contrato mínimo de uma ficha CTI

| Campo | Regra de preenchimento |
|---|---|
| ID e título | Chave estável e nome não sensacionalista |
| Data do evento | Quando a atividade ocorreu; aceitar intervalo ou desconhecida |
| Data da fonte | Quando o conteúdo foi publicado/revisado |
| Região e setor | Registrar apenas o que a fonte divulga |
| Família / campanha / software | Não confundir software, operação e grupo |
| Ativo e processo | PLC/RTU/HMI/EWS/SIS, quando confirmados |
| Impacto TI | Indisponibilidade ou comprometimento empresarial documentado |
| Impacto OT | Distinguir **confirmado**, **não confirmado** e **não aplicável** |
| TTPs / ATT&CK ICS | ID da técnica com URL e trecho verificável |
| Telemetria | Evidência requerida para investigar ou detectar o comportamento |
| Confiança | A, B, C ou D conforme [classificação](inteligencia-ameacas.md) |
| Controles | Medida, risco de aplicação, responsável operacional |
| Direitos | Link à origem; não copiar relatório proprietário |

## Pipeline de curadoria, não de ataques

1. **Ingestão:** monitorar páginas públicas do NIST, CISA, MITRE, INL e fontes de pesquisa. Registrar URL, versão e data de acesso.
2. **Deduplicação:** associar múltiplas fontes ao mesmo evento, preservando discordâncias e data de cada relato.
3. **Triagem:** confirmar que produto, versão, exposição e consequência têm relação efetiva com OT; CVE isolada não prova exploração.
4. **Normalização:** associar setor, ativo, protocolo, comportamento, evidência e consequência operacional.
5. **Enriquecimento:** vincular advisories, MITRE, CVEs e possíveis IOCs sem convertê-los em verdade definitiva. EPSS é probabilidade estatística de exploração, não avaliação direta de dano físico.
6. **Revisão humana:** analista de CTI mais engenharia OT/safety para alterações recomendadas em produção.
7. **Publicação:** atualizar o [atlas de casos](casos-ot/README.md) e [catálogo estruturado](../catalogo/casos.json), com proveniência.
8. **Reavaliação:** corrigir atribuição, impacto e mitigação quando nova evidência contradisser a anterior.

## Threat-informed defense: métrica útil

| Pergunta | Métrica | Limitação |
|---|---|---|
| Há fontes e observáveis suficientes? | cobertura de evidências por caso | volume de links não mede qualidade |
| A técnica tem fonte para o mapeamento? | proporção de mapeamentos revisados | mapeamento não implica detecção |
| A equipe tem observabilidade? | ativos e fluxos cobertos por telemetria | inventário é frequentemente incompleto |
| O alerta é confiável? | falso positivo, precisão e atraso de detecção | exige ground truth independente |
| A resposta preserva o processo? | risco de efeito colateral e recuperação | bloqueio automático pode comprometer disponibilidade |

**Nunca converter automaticamente um IOC de terceiro em tráfego “malicioso”**, nem derivar automaticamente um playbook executável de uma técnica. Um endereço IP, hash ou CVE não é, sozinho, uma descrição de comportamento observável em uma planta.

## Exercício de revisão (sem rede de ataque)

**Situação:** relatório menciona interrupção da produção após ransomware empresarial, mas não apresenta logs de PLC. Classifique como efeito operacional em empresa industrial, mantendo **comprometimento de controle não confirmado**. Investigue dependências TI/OT, decisão de parada e preservação de evidências.

## Referências

- [NIST SP 800-82 Rev. 3 — final (2023)](https://csrc.nist.gov/pubs/sp/800/82/r3/final)
- [NIST SP 800-82 Rev. 4 — rascunho público (2026)](https://csrc.nist.gov/Projects/operational-technology-security/publications)
- [ATT&CK for ICS](https://attack.mitre.org/matrices/ics/)
- [CyOTE Insights / INL](https://cyote.inl.gov/tools/cyote-insights/)
- [NSA/CISA — Control System Defense: Know the Opponent](https://www.nsa.gov/Press-Room/Digital-Media-Center/Document-Gallery/igphoto/2003083007/)
