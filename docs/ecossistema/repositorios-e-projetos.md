# 11 / Repositórios e projetos externos selecionados

**Critério de inclusão:** contribuição para **inteligência, visibilidade, arquitetura, educação e pesquisa OT global**. Frameworks centrados em topologias, scripts e runners de Mininet são deliberadamente tratados no [projeto separado](../separacao-de-escopos.md).

| Projeto | Origem | Papel no Caldeira | Ressalva |
|---|---|---|---|
| [CyOTE Insights](https://github.com/idaholab/Insights) | Idaho National Laboratory | Banco de casos históricos, observáveis e mapeamento ATT&CK for ICS | Reconstrução analítica; ler premissas e incerteza do PAR |
| [ICSNPP](https://github.com/cisagov/ICSNPP) | CISA / INL | Vocabulário técnico de protocolos e observabilidade Zeek | Repositório agregador com módulos e níveis diferentes de parsing |
| [Cyber4OT](https://github.com/krzysztof-cabaj/Cyber4OT) | Cabaj et al. | Evidência experimental de rede para discussões de detecção | Incidente **simulado** em testbed |
| [HAI](https://github.com/icsdataset/hai) | Autores do dataset HIL | Comportamento físico e avaliação de anomalias | Séries temporais não são PCAPs |
| [Conpot](https://github.com/mushorg/conpot) | MushMush Foundation / comunidade | Estudo de deception OT e coleta de observáveis | Honeypot, não representa processo físico real |
| [OpenPLC Runtime](https://github.com/Autonomy-Logic/openplc-runtime) | Autonomy Logic | Referência de software PLC e gestão de lógica | Não é evidência de que um PLC de produção possua as mesmas propriedades |
| [opcua-asyncio](https://github.com/FreeOpcUa/opcua-asyncio) | FreeOpcUa | Referência de implementação OPC UA | Biblioteca, não um relatório de incidente |
| [awesome-ics-writeups](https://github.com/neutrinoguy/awesome-ics-writeups) | Neutrinoguy / comunidade | Descoberta de artigos e análises técnicas | **Índice secundário**; verificar cada estudo na publicação de origem |
| [Getting Started with ICS](https://github.com/utilsec/Getting_Started_with_ICS) | utilsec | Material introdutório para TI e OT | Conteúdo de terceiros; não reempacotar PDFs |
| [NIST OT Security](https://csrc.nist.gov/Projects/operational-technology-security/publications) | NIST | Guias, backups, acesso remoto e atualizações normativas | Distinguir rascunhos de edições finais |

## Como aproveitamos essas referências

- **Referenciar** projeto, versão e mantenedor, não copiar seu README integral.
- **Relacionar** cada recurso a protocolo, tipo de evidência e setor.
- **Converter** relatórios de terceiros em síntese original com limites.
- **Separar** produção de evidências científicas de recursos de emulação/testes.
- **Respeitar** licenças e termos de redistribuição; links não são autorização para espelhamento.

## Fora do escopo desta coleção

MiniCPS, NEFICS, Mininet-Sec, MininetGym, MECInOT e implementações de topologias/runners específicas do Mininet são **referências do repositório mininet**, não dependências ou módulos do Caldeira.

Projetos citados em pesquisas sem comprovação suficiente de repositório, autoria, licenciamento ou validade das afirmações ficam em **triagem**, não entram como fontes aprovadas.

## Próximos estudos institucionais

- [NIST SP 1800-45 — acesso remoto OT em água e saneamento](https://csrc.nist.gov/Projects/operational-technology-security/publications).
- [NIST SP 1339 — OT Backup Quick Start Guide](https://csrc.nist.gov/Projects/operational-technology-security/publications).
- [ISA/IEC 62443 — normas e responsabilidades](https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards).
- [SUTD iTrust — datasets e testbeds](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/).
