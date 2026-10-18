# Arquitetura editorial / Caldeira e Mininet são projetos separados

~~~mermaid
flowchart TB
    S["Fontes globais públicas / pesquisadores / padrões"] --> C["CALDEIRA CYBER OT"]
    C --> CTI["Threat intelligence e incidentes"]
    C --> DAT["Datasets e bibliografia"]
    C --> NOR["Normas, fornecedores e recomendações"]
    CTI --> Q["Perguntas de pesquisa, não código executável"]
    Q -. "referência documental" .-> M["MININET SEC LAB / projeto independente"]
    M --> E["Testes em rede emulada e evidência técnica"]
    E -. "achados agregados e revisados" .-> C
~~~

| Capacidade | CaldeiraCyberOT | mininet |
|---|---|---|
| Casos reais e cadeia de evidência | **Sim: repositório principal** | Referência aos casos, quando útil |
| Cenário global e risco por setor | **Sim** | Não |
| ATT&CK for ICS, normas e guias | **Sim: revisão conceitual** | Mapeamento operacional de experimentos |
| Inventário de fornecedores | **Sim** | Não |
| Catálogo de datasets e suas limitações | **Sim: curadoria e DOI** | Aquisição, extração e avaliação |
| OpenPLC, OPC UA e parsers | **Visão tecnológica e referências** | Configuração/integração de laboratório |
| Topologias, namespaces, Mininet-Sec | Não | **Sim** |
| Scripts, captures, simulações e testes | Não | **Sim** |
| Detecção e telemetria | **Método e hipóteses** | **Runner, detector e evidência** |
| Publicações com análise independente | **Sim** | Metodologia experimental do próprio projeto |

**Regra de fronteira:** sem pasta de scripts de ataque, sem simuladores embutidos, sem clonagem de suites externas ou geração automática de ataques dentro do Caldeira. O repositório permanece uma base de conhecimento pesquisável e auditável.

**Links:** [CaldeiraCyberOT](https://github.com/Ridd1kulusC0d3r/CaldeiraCyberOT) · [mininet](https://github.com/Ridd1kulusC0d3r/mininet)
