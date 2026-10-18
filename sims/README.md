# Backends simulados / Interfaces planejadas

**Estado: documentação de arquitetura.** O `core/` executa apenas avaliação de **fixtures JSON fictícias**. Nenhuma das ferramentas abaixo foi instalada, encapsulada ou integrada neste repo.

| Ferramenta | Nível didático | Interesse defensivo | Integração |
|---|---|---|---|
| [Mininet (repo independente)](https://github.com/Ridd1kulusC0d3r/mininet) | Rede e fronteiras de zonas | Analisar arquiteturas e políticas de fluxo | **Somente link** |
| [OpenPLC](https://github.com/thiagoralves/OpenPLC_v3) | L1 / PLC | Entender lógica de controle, em bancada segura | Planejada |
| [ScadaBR](https://www.scadabr.com.br/) | L2 / SCADA | Contexto e visibilidade de supervisão | Planejada; verificar licença e manutenção |
| [PyModbus](https://github.com/pymodbus-dev/pymodbus) | Modelagem de protocolos | Fontes didáticas de eventos, nunca produção | Planejada |
| [GRFICS](https://github.com/Fortiphyd/GRFICSv2) | L0-L2 | Representação didática de processo físico | Planejada; validar manutenção/licença |
| [Conpot](https://github.com/mushorg/conpot) | Telemetria de engano | Avaliar e enriquecer registros de observação | Planejada; não implantar infraestrutura acessível publicamente |
| [python-snap7](https://github.com/gijzelaerr/python-snap7) | Protocolo Siemens S7 | Estudo de formato e registros, sem controle ativo | Pesquisa futura |

### Critérios antes de uma integração

1. Manutenção ativa, licença verificável, compatibilidade, issues de segurança.
2. Isolamento, ausência de tráfego ativo para dispositivos industriais e controle de dados.
3. Só exportar **metadados anonimizados e sintéticos** ao núcleo durante o MVP.
4. Adicionar testes unitários sem root e sem hardware.
5. Não declarar um backend funcional porque seu README foi criado.

## Status de implementação

**Implementado:** backend local implícito que lê JSON e detecta anomalias de política. **Não implementados:** listeners, honeypots em rede, emuladores de física, pacotes PLC/SCADA e integração Mininet.