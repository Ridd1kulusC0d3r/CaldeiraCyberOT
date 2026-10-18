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