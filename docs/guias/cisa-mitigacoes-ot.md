# CISA · Cinco mitigações prioritárias para segurança OT

**Fonte principal:** [Primary Mitigations to Reduce Cyber Threats to Operational Technology](https://www.cisa.gov/resources-tools/resources/primary-mitigations-reduce-cyber-threats-operational-technology), **6 de maio de 2025**. Autoria conjunta: **CISA, FBI, EPA e DOE** (Estados Unidos). [Ficha PDF oficial](https://www.cisa.gov/sites/default/files/2025-05/fact-sheet-primary-mitigations-to-reduce-cyber-threats-to-operational-technology-508c.pdf).

**Natureza:** síntese **independente** para estudo e planejamento defensivo. Não é transcrição integral, prescrição regulatória fora dos EUA, procedimento de operação nem autorização para mudar sistemas reais.

## Por que este documento importa?

O alerta reúne práticas básicas contra atividades direcionadas a sistemas **OT/ICS conectados à internet**. Ele é útil como *baseline* de perguntas para inventário, conectividade, identidades, arquitetura, resposta e continuidade.

| Prioridade da orientação | Objetivo defensivo | Evidência que uma equipe pode revisar sem provocar alteração na planta | Responsáveis para validação |
|---|---|---|---|
| **01 · Reduzir exposição pública** | Minimizar serviços OT desnecessariamente acessíveis | Inventário autorizado de ativos e fluxos, registros de publicação de serviços, avaliação formal de dependências | OT + TI + redes |
| **02 · Eliminar credenciais padrão** | Reduzir risco de comprometimento por autenticação fraca | Política de gestão de credenciais, evidência administrativa de revisão, exceções registradas | Dono do ativo + IAM + fornecedor |
| **03 · Fortalecer acesso remoto** | Limitar e tornar auditáveis acessos de técnicos/terceiros | Inventário de caminhos remotos, MFA resistente a phishing quando suportado, perfis de privilégio, histórico de sessão | OT + IAM + integradores |
| **04 · Segmentar IT/OT** | Reduzir propagação entre ambientes e proteger serviços de controle | Modelo de zonas e conduítes, fluxos permitidos, registros de aprovação e documentação de DMZ | Eng. redes + engenharia industrial |
| **05 · Preservar operação manual segura** | Sustentar processos essenciais quando ferramentas digitais estiverem indisponíveis | Procedimentos aprovados, treinamento formal, exercícios autorizados de continuidade e limites de operação | Segurança de processo + operações + gestão de crises |

> **Importante:** “reduzir exposição” não significa desligar conexões de sistemas críticos sem planejamento. Testes de contingência, operação manual, credenciais ou segmentação requerem aprovação dos responsáveis, análise de risco e procedimentos específicos da instalação.

## Cinco achados para uma revisão baseada em evidências

### 1. Exposição à internet
A orientação propõe eliminar acesso público desnecessário a ativos OT. **Pergunta ao time:** sabemos quais serviços foram aprovados e qual processo físico depende deles?

### 2. Credenciais
A publicação destaca credenciais de fábrica e senhas previsíveis. **Pergunta:** existe processo de gestão de segredos compatível com o ciclo de manutenção industrial e com acesso de emergência?

### 3. Acesso remoto
O documento orienta caminhos mais protegidos, autenticação forte, menor privilégio e desativação de contas não utilizadas. **Pergunta:** conseguimos relacionar cada sessão autorizada a pessoa, janela e ordem de trabalho?

### 4. IT/OT e DMZ
A segmentação reduz potenciais efeitos de incidentes entre redes. **Pergunta:** conhecemos fluxos indispensáveis ao processo e sabemos revisar exceções antes de alterá-los?

### 5. Operação manual
Continuidade e segurança física precisam contemplar falhas ou indisponibilidade dos sistemas digitais. **Pergunta:** planos de contingência e métodos manuais são **viáveis para aquela planta** e já foram aprovados em exercícios seguros?

## Aplicabilidade aos cases do Caldeira

| Case | Relação com as recomendações CISA | Limitação |
|---|---|---|
| [CAL-LAB-001 · Modbus](../../cases/README.md) | Detectar **desvio sintético** em origens autorizadas, associado a governança de identidade e controles de alteração | Não atesta troca de senha nem comando Modbus em PLC real |
| [CAL-LAB-002 · IT/OT](../../cases/README.md) | Detectar fluxo fictício não previsto na matriz de fronteira, associado a segmentação | Não prova acesso indevido, intrusão ou eficácia de firewall |
| [Dossiês reais](../casos-ot/README.md) | Relacionar relatos públicos a dependências, acessos e continuidade | Nem toda interrupção fabril implica comprometimento ICS |

### Matriz de leitura e prioridade

- **Alta prioridade editorial:** inventário e exposição, fluxos IT/OT, acesso de terceiros, manutenção de operação manual segura.
- **Prioridade operacional real:** só pode ser definida por processo, impacto físico, riscos ambientais, disponibilidade, dependências e requisitos aplicáveis.

## Fontes, licença e limites

- [Página da orientação no site CISA](https://www.cisa.gov/resources-tools/resources/primary-mitigations-reduce-cyber-threats-operational-technology)
- [Documento original em PDF](https://www.cisa.gov/sites/default/files/2025-05/fact-sheet-primary-mitigations-to-reduce-cyber-threats-to-operational-technology-508c.pdf)
- [NIST SP 800-82 Rev. 3](https://csrc.nist.gov/pubs/sp/800/82/r3/final)
- [SANS Five ICS Cybersecurity Critical Controls](https://www.sans.org/white-papers/five-ics-cybersecurity-critical-controls)

**Verificação editorial:** 18/10/2026. A página CISA pode apresentar bloqueio de coleta automatizada; a existência da publicação e seu conteúdo central foram corroborados pela versão PDF oficial indexada. Não hospedar cópia sem conferir direitos de redistribuição.
