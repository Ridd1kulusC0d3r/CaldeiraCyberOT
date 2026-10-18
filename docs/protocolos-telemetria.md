# 10 / Protocolos industriais e telemetria defensiva

> **Protocolo ≠ risco isolado.** Porta exposta, uso legítimo, configuração de autenticação, papel do ativo e consequência operacional devem ser avaliados em conjunto.

| Tecnologia | Contexto OT | Observáveis defensivos | Cuidados de interpretação |
|---|---|---|---|
| **Modbus TCP** | PLC/RTU, supervisão e controle | origem/destino, função, padrão de leitura/escrita, frequência, valores permitidos | escrita não é necessariamente anômala; validar papel e janela |
| **OPC UA** | Interoperabilidade, gateways e SCADA | certificados, sessões, endpoints, método de segurança, alterações de nós e auditoria | conexão a porta típica não prova OPC UA completo; tráfego criptografado exige logs de endpoint |
| **DNP3** | Telecontrole e utilities | mestre/outstation, mudanças de estado, contadores e janelas de controle | não transportar conclusões de TCP genérico para mensagens de aplicação |
| **IEC 60870-5-104** | Telecontrole elétrico | sequência de eventos, origem de comandos, integridade e consistência de estados | associar objetos e papéis ao desenho da subestação |
| **EtherNet/IP e CIP** | Automação industrial | inventário de dispositivos, sessões e tipos de operações observadas | Ethernet/IP não é sinônimo de internet pública |
| **S7comm** | Ecossistema Siemens | sessões de engenharia, mudanças de operação e inventário | comportamento válido varia por produto e versão |
| **IEC 61850** | Subestações | eventos e supervisão dos fluxos do ambiente, trilhas de configuração | latência e requisitos do processo exigem avaliação especializada |

### Quatro camadas de confiança

~~~mermaid
flowchart LR
  NET["Rede: quem comunica"] --> PRO["Protocolo: qual operação"]
  PRO --> APP["Aplicação: qual autorização"]
  APP --> PHY["Processo: qual consequência"]
~~~

O detector ideal correlaciona **identidade do ativo**, **operação**, **autorização**, **janela de manutenção**, **estado do processo** e **qualidade da telemetria**. Pacotes isolados têm pouco contexto para distinguir manutenção planejada de atividade indevida.

### Perguntas de engenharia defensiva

1. Quais PLCs/RTUs/HMIs são conhecidos e qual inventário independente os confirma?
2. Quais sistemas podem iniciar sessões e alterar parâmetros, segundo o processo de mudança?
3. Qual fonte registra alterações de lógica, firmware, contas, permissões e alarmes?
4. Existem medições independentes para perceber perda/manipulação de visibilidade?
5. Uma ação automática de contenção poderia prejudicar segurança física ou disponibilidade?

### Fontes confiáveis

- [CISA ICSNPP — parsers OT para Zeek](https://github.com/cisagov/ICSNPP), incluindo extensões de logs Modbus e DNP3 e parsers especializados. **Não** pressupor cobertura idêntica de todos os campos para todos os protocolos.
- [CISA ICS Network Protocol Parsers — página institucional](https://www.cisa.gov/resources-tools/services/ics-network-protocol-parsers).
- [NIST SP 800-82 Rev. 3](https://csrc.nist.gov/pubs/sp/800/82/r3/final).
- [Mandiant — INCONTROLLER](https://cloud.google.com/blog/topics/threat-intelligence/incontroller-state-sponsored-ics-tool/).
- [MITRE — Modify Alarm Settings T0838](https://attack.mitre.org/techniques/T0838/) e [Detection Strategy DET0777](https://attack.mitre.org/detectionstrategies/DET0777/).

Este documento é **referência de observabilidade**. Implementação e teste de redes emuladas são responsabilidade do repositório independente [mininet](https://github.com/Ridd1kulusC0d3r/mininet).
