# Cases / Detecção e inteligência OT

**Não confundir** [atlas de incidentes reais](../docs/casos-ot/README.md) com estes **casos sintéticos de análise defensiva**.

| Case | Arquivo | Objetivo | Saída esperada |
|---|---|---|---|
| **CAL-LAB-001** | [modbus-policy.json](fixtures/modbus-policy.json) | Identificar origem não permitida em metadado de escrita Modbus fictícia | 1 achado `CAL-DET-OT-001` |
| **CAL-LAB-002** | [boundary-policy.json](fixtures/boundary-policy.json) | Identificar fluxo IT→OT não previsto em matriz fictícia | 1 achado `CAL-DET-IT-001` |

## Reprodução local sem rede

```bash
python -m core.runner cases/fixtures/modbus-policy.json
python -m core.runner cases/fixtures/boundary-policy.json
python -m unittest discover -s tests -v
```

A saída de cada caso inclui **payload**, **digest SHA-256** e **finding(s)** com IDs estáveis. A integridade cobre o relatório local gerado, não autenticação de equipamentos.

### Validação analítica

A primeira regra ilustra uma condição compatível com o exame de **T1692.001**, não comprova a técnica em incidente real. A segunda identifica um **desvio de política**, não exploração nem pivô confirmado. Ambas exigiriam enriquecimento e revisão humana antes de qualquer ação real.

**Backends:** fixtures versionadas são a única entrada executável implementada. Consulte [simuladores em avaliação](../sims/README.md).