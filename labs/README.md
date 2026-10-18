# 06 / Laboratórios e casos de estudo defensivos

A missão desta área é converter perguntas de OT security em exercícios **seguros, isolados, observáveis e reproduzíveis**. Nenhum laboratório pressupõe conexão com dispositivos de produção.

## Catálogo inicial

| ID | Cenário | O que se aprende | Resultado esperado |
|---|---|---|---|
| **LAB-01** | Inventário a partir de dados sintéticos de tráfego industrial | Identificar ativos conhecidos e desconhecidos em registros simulados | Mapa de ativos e lacunas |
| **LAB-02** | Comparação entre arquitetura plana e segmentada, em simulador | Raciocinar sobre zonas, conduítes e fluxos permitidos | Diagrama, matriz de fluxos |
| **LAB-03** | Anomalias simuladas de comunicação SCADA | Criar hipótese de detecção sem interagir com CLP real | Regra conceitual e evidências |
| **LAB-04** | Tabletop de dependência TI/OT | Coordenar resposta, safety e continuidade | RACI, cronologia e decisões |
| **LAB-05** | Avaliação de um relatório de ameaças | Relacionar alegações ao grau de evidência | Ficha CTI com incertezas |

### Fluxo de produção do caso

~~~mermaid
flowchart LR
  A["Hipótese e objetivo"] --> B["Dataset sintético"]
  B --> C["Topologia isolada"]
  C --> D["Observação e validação"]
  D --> E["Lições e mitigação"]
~~~

## Modelo de entrega de caso

1. **Objetivo** e contexto do processo modelado.
2. **Escopo seguro** e separação completa da rede real.
3. **Diagrama** da topologia didática.
4. **Dados sintéticos** e suas limitações.
5. **Observações defensivas**, hipóteses, evidências.
6. **Critérios de aprovação**, falso positivo e lacunas.
7. **Fontes**, versão do cenário e revisão por pares.

## Conexão com simuladores

O Mininet pode representar **topologias IP, segmentação e políticas de fluxo**, mas **não reproduz por si só o comportamento físico de um PLC, uma planta ou um SIS**. Não apresentar uma simulação de rede como validação de segurança de processo. Priorizar roteiros de observação, análise de logs sintéticos e avaliações por cenários.

Comece com [NIST SP 800-82r3](https://csrc.nist.gov/pubs/sp/800/82/r3/final) e [ATT&CK for ICS](https://attack.mitre.org/matrices/ics/) para formular perguntas de defesa.
## Escopo dos estudos aplicados

O **Caldeira** hospeda exercícios de **tabletop, análise de relatório, revisão de evidência, política de acesso e mapeamento de telemetria**. Implementações de redes, ferramentas de ataque e geração/captura de pacotes pertencem ao [repositório Mininet](https://github.com/Ridd1kulusC0d3r/mininet).

| Roteiro do Caldeira | Referência | Entrega não operacional |
|---|---|---|
| **LAB-06 · Incident reconstruction** | [Industroyer2](../docs/casos-ot/README.md#cal-case-005--industroyer2-2022) | Linha do tempo e pontos de telemetria relevantes |
| **LAB-07 · SIS resilience review** | [TRITON](../docs/casos-ot/README.md#cal-case-003--triton--trisis-2017) | Checklist de segregação, mudança e segurança de processo |
| **LAB-08 · Protocol-aware monitoring** | [FrostyGoop](../docs/casos-ot/README.md#cal-case-006--frostygoop-2024) | Hipótese de alerta autorizada/indevida, sem comandos reais |
| **LAB-09 · TI versus OT impact** | [JBS](../docs/casos-ot/README.md#cal-case-007--jbs-2021) | Árvore de dependência empresarial/industrial e RACI |
| **LAB-10 · Dataset validity** | [Cyber4OT e HAI](../docs/datasets-ot.md) | Matriz de origem, rótulos, vieses e integridade |

Para cada exercício, anexar fontes, justificativas, limites e revisão humana. Ver [separação de escopos](../docs/separacao-de-escopos.md).
