# COMECE AQUI / Caldeira Cyber OT Labs

[← README](README.md) · [Arquitetura](docs/arquitetura-labs.md) · [Casos](cases/README.md) · [Atlas global](docs/casos-ot/README.md)

## Trilha rápida em 5 minutos

**Requisitos:** Python 3.10+; nenhuma dependência externa, conta em nuvem, root ou acesso à rede necessários.

```bash
python -m unittest discover -s tests -v
python -m core.runner cases/fixtures/modbus-policy.json
python -m core.runner cases/fixtures/boundary-policy.json
```

Cada execução lê **apenas arquivos JSON fictícios** e exibe em stdout um envelope com alertas e resumo de integridade SHA-256. Não abre sockets nem envia tráfego, e não altera ativos.

## O que observar

1. Em `CAL-LAB-001`, há um registro de escrita Modbus que viola a lista fictícia de fontes autorizadas. A regra informa um **desvio de política**, não evidência de invasão ou alteração física.
2. Em `CAL-LAB-002`, há um fluxo IT→OT fora da matriz declarada. O detector **não** classifica esse metadado isolado como pivô, movimento lateral ou ataque.
3. Altere um campo de uma *cópia* do envelope emitido sem recalcular o digest: `core.evidence.verify` deixará de validar o hash. **SHA-256 sozinho não comprova autoria.**

## O que já existe

- `core/detectors/ot/modbus.py` → detecção pura de regra de escrita fora do baseline.
- `core/detectors/it/boundary.py` → identificação de fluxo entre zonas sem autorização cadastrada.
- `core/evidence.py` → JSON canônico, digest SHA-256 e verificação.
- `core/runner.py` → leitura e avaliação de fixtures estáticas offline.
- `core/intel/attack_ics.json` → catálogo de referências ao ATT&CK for ICS, sem atribuição automática.
- `tests/test_core.py` → testes de funcionamento e integridade.

## Novo braço: MANÔMETRO

KPIs de OT sobre exportações sintéticas da integração Claroty xDome → Elastic, com deduplicação, ATT&CK for ICS v20.0 e saúde da coleta. Comece por [manometro/COMECE-AQUI.md](manometro/COMECE-AQUI.md).

## O que está no roadmap, mas não foi implementado

OpenPLC, ScadaBR, Conpot, GRFICS, protocolos DNP3/S7/IEC-104 e integração com Mininet. Estão **documentados como possíveis fontes futuras de telemetria**, sem execução incorporada. O projeto [Mininet](https://github.com/Ridd1kulusC0d3r/mininet) permanece independente.

**Safety:** nunca usar fixtures ou inferências deste laboratório para decisões automáticas em processos reais. Revisão de engenharia OT é obrigatória para aplicações em produção.