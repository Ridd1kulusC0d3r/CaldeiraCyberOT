# 07 / Atlas de casos reais em Cyber OT

> **Princípio:** ocorrência documentada, capacidade de uma ferramenta e hipótese de laboratório são coisas diferentes. Este atlas reúne os dois primeiros **sem** promover reprodução operacional de ataques.

**Navegação:** [Dossiês](#dossiês-analíticos) · [Comparação](#matriz-comparativa) · [Método](../metodologia-cti-ot.md) · [Fontes](../../relatorios/fontes-primarias-ot.md)

## Matriz comparativa

| Caso | Evento | Ambiente | Situação da evidência | Pergunta defensiva |
|---|---:|---|---|---|
| Ucrânia / BlackEnergy | 2015 | Distribuição de energia | Incidente operacional documentado; reconstrução exige múltiplas fontes | Quais dependências de acesso remoto e supervisão permitem interromper a operação? |
| Industroyer / CrashOverride | 2016 | Distribuição elétrica | Incidente com impacto operacional documentado | Que sinais diferenciam comando de controle autorizado de atividade inesperada? |
| TRITON / TRISIS | 2017 | SIS / segurança de processo | Framework identificado em investigação de incidente | Há governança, monitoramento e independência adequados para o SIS? |
| INCONTROLLER / PIPEDREAM | 2022 | PLCs, OPC UA e automação | **Ferramentas analisadas; uso efetivo em ataque à planta não demonstrado pela fonte original** | O inventário e os controles consideram diferentes fornecedores e protocolos? |
| Industroyer2 | 2022 | Energia elétrica / IEC-104 | Tentativa de operação disruptiva identificada e investigada | Como validar integridade, autorização e cronologia das ações de controle? |
| FrostyGoop | 2024 | Aquecimento distrital / Modbus TCP | Incidente relacionado a interrupção de serviço segundo Dragos e MITRE | A telemetria distingue sessão legítima de modificação indevida de parâmetro? |
| JBS | 2021 | Indústria alimentícia | Ransomware corporativo e interrupção operacional; **não inferir comprometimento de PLC** | Como dependências de TI e decisões de continuidade afetam operações industriais? |

## Dossiês analíticos

### CAL-CASE-001 · Ucrânia / BlackEnergy (2015)
- **Natureza:** incidente histórico em infraestrutura elétrica, com operações afetadas.
- **Evidências:** reconstruções de pesquisadores e o conjunto histórico [CyOTE Insights / INL](https://cyote.inl.gov/tools/cyote-insights/).
- **Sinais investigativos:** administração remota, mudanças não planejadas em estações operacionais, continuidade dos registros de operação, capacidade de recuperação.
- **Ressalva:** BlackEnergy não deve ser confundido com todo e qualquer mecanismo físico responsável pela interrupção; separe ações humanas, acesso e efeitos operacionais na linha do tempo.
- **Estudo sugerido:** mapa de dependências, pontos de observação e plano de resposta conjunto TI/OT.

### CAL-CASE-002 · Industroyer (2016)
- **Natureza:** malware relacionado a interrupções no setor elétrico.
- **Evidências:** caso histórico indexado em [CyOTE Insights](https://cyote.inl.gov/tools/cyote-insights/) e [MITRE ATT&CK for ICS](https://attack.mitre.org/matrices/ics/).
- **Sinais investigativos:** origem e autorização de comandos, mudanças no estado de equipamentos, perda de supervisão e reconstrução temporal.
- **Ressalva:** não generalizar um caso específico para todas as subestações ou protocolos.

### CAL-CASE-003 · TRITON / TRISIS (2017)
- **Natureza:** incidente envolvendo sistema instrumentado de segurança (SIS).
- **Fonte primária técnica:** [Mandiant, 14/12/2017](https://cloud.google.com/blog/topics/threat-intelligence/attackers-deploy-new-ics-attack-framework-triton).
- **Fato sustentado:** a investigação identificou software projetado para interagir com controladores Triconex de segurança; a fonte discute interrupção operacional e suas hipóteses sobre intenção.
- **Sinais investigativos:** integridade de aplicações de engenharia, eventos de manutenção, independência entre controle de processo e funções de segurança.
- **Ressalva:** intenção presumida pelo analista não equivale a consequência física comprovada.

### CAL-CASE-004 · INCONTROLLER / PIPEDREAM (2022)
- **Natureza:** conjunto de ferramentas direcionadas a tecnologias ICS.
- **Fontes:** [Mandiant, 13/04/2022](https://cloud.google.com/blog/topics/threat-intelligence/incontroller-state-sponsored-ics-tool/) · [MITRE S1045](https://attack.mitre.org/software/S1045/) · [CISA AA22-103A](https://www.cisa.gov/news-events/cybersecurity-advisories/aa22-103a).
- **Fato sustentado:** análise de capacidades voltadas a componentes Schneider Electric, Omron e OPC UA, entre outros.
- **O que NÃO está demonstrado na fonte de lançamento:** invasão consumada de uma instalação industrial específica com esse toolkit.
- **Sinais investigativos:** alteração de configuração, mudanças de sessão e permissões, atividades inesperadas de estação de engenharia.
- **Resultado de estudo:** matriz de exposição por **produto e versão afetados**, não uma atribuição automática a qualquer empresa que utilize Modbus.

### CAL-CASE-005 · Industroyer2 (2022)
- **Natureza:** atividade contra fornecedor de energia na Ucrânia.
- **Fonte primária técnica:** [ESET Research e CERT-UA, 12/04/2022](https://www.welivesecurity.com/2022/04/12/industroyer2-industroyer-reloaded/).
- **Fato sustentado:** investigação de tentativa disruptiva com componente ICS e ferramentas de apagamento; análise de comunicação IEC-104.
- **Sinais investigativos:** cronologia de comandos, credenciais de operação, integridade dos sistemas supervisórios e evidências de recuperação.
- **Ressalva:** uma tentativa de interrupção não deve ser contabilizada automaticamente como apagão confirmado.

### CAL-CASE-006 · FrostyGoop (2024)
- **Natureza:** campanha com impacto em serviço de aquecimento distrital na Ucrânia.
- **Fontes:** [Dragos, intelligence brief](https://hub.dragos.com/report/frostygoop-ics-malware-impacting-operational-technology) · [MITRE Campaign C0041](https://attack.mitre.org/campaigns/C0041/) · [MITRE Software S1165](https://attack.mitre.org/software/S1165/).
- **Fato sustentado:** incidentes de janeiro de 2024 e uso de Modbus TCP para interagir com sistemas de controle; a atribuição causal completa deve ser lida nos termos da avaliação publicada.
- **Técnica documentada:** [T0836 — Modify Parameter](https://attack.mitre.org/techniques/T0836/).
- **Sinais investigativos:** mudanças de parâmetro fora da janela autorizada, divergência entre medições e histórico, exposição de serviços de controle.
- **Ressalva:** o fato de um comando estar no formato correto não o torna autorizado.

### CAL-CASE-007 · JBS (2021)
- **Natureza:** ransomware em organização industrial, com interrupção de operações.
- **Referência para estudo comparativo:** [CyOTE Insights / INL](https://cyote.inl.gov/tools/cyote-insights/).
- **Classificação Caldeira:** **impacto na continuidade de uma empresa industrial**, não evidência automática de manipulação de lógica de PLC.
- **Sinais investigativos:** dependências de identidade, ERP, agendamento, logística, acesso de fornecedores e plano de continuidade.
- **Pergunta central:** como uma disrupção de TI chega à operação sem que exista comprometimento demonstrado de sistemas de controle?

## Como ler cada caso

1. Separar **ano do evento**, **data da publicação** e **última atualização da fonte**.
2. Classificar: incidente com efeito operacional, ferramenta descoberta, alegação sem verificação ou exercício acadêmico.
3. Registrar **quem observou**, **quais evidências são públicas** e **que parte permanece incerta**.
4. Vincular técnicas ATT&CK somente quando a fonte sustentar o comportamento; nunca transformar uma tática em prova de autoria.
5. Produzir uma **hipótese defensiva** verificável por logs, configuração, engenharia e segurança de processo, sem depender de reproduzir interferência em infraestrutura real.

> **Limite editorial:** não hospedamos malware, procedimentos de sabotagem, exploits ou playbooks de interferência em equipamentos industriais. O foco é inteligência, prevenção, detecção e resiliência.
