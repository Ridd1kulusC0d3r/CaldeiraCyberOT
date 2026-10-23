# Relatório de testes · MANÔMETRO

[← README do braço](README.md)

| Item | Valor |
|---|---|
| Data | 23/10/2026 (America/Sao_Paulo) |
| Ambiente | Workspace Linux em nuvem (kernel 6.18), sem acesso de rede pelo código testado |
| Interpretadores | Python 3.13.17 e Python 3.11.17 |
| Comando | `python -m unittest discover -s tests -v` |
| Resultado | **25 testes, 0 falhas, 0 erros** nas duas versões (9 do núcleo + 16 do Manômetro) |
| Determinismo | Duas execuções do demo (2026-01 → 2026-10) geraram o mesmo digest `771bc041173c2d25…48fa` |
| Isolamento | Nenhum import de `socket`, `urllib`, `http` ou `subprocess` em `manometro/` |
| Exportação demo | `fixtures/demo-xdome.json` · SHA-256 `c7ef9424afd152c3…6c75` · 1.033 documentos |
| Catálogo | `ics-attack-20.0.json` oficial · SHA-256 `c9ca0ce523a1b5e5…1183` · 12 / 78 / 26 |

## O que cada grupo prova

| Grupo | Testes | Garante |
|---|---:|---|
| `CatalogoTest` | 3 | Contagens oficiais do v20.0, ordem das táticas, remapeamento de revogados, ID fora do ICS, técnica multitática |
| `DedupTest` | 3 | Estado mais recente vence; fan-out só do snapshot vigente; leitura de campo achatado e aninhado |
| `DemoTest` | 9 | Envelope íntegro e adulteração detectada; números do demo; matriz separa comportamento; baseline; saúde; seletor de período; período inválido; HTML sem recursos externos; entrada não mutada |
| `TravaSinteticaTest` | 1 | Exportação sem `synthetic: true` é recusada |

O GitHub Actions (`.github/workflows/ot-labs-tests.yml`) repete a bateria em Python 3.12 a cada push ou PR que toque `core/`, `cases/`, `manometro/` ou `tests/`.

## Saída da execução (Python 3.13)

```text
test_approved_boundary_not_alerted (test_core.CoreTest.test_approved_boundary_not_alerted) ... ok
test_boundary_finding (test_core.CoreTest.test_boundary_finding) ... ok
test_hash_determinism_and_tamper (test_core.CoreTest.test_hash_determinism_and_tamper) ... ok
test_legitimate_write_not_alerted (test_core.CoreTest.test_legitimate_write_not_alerted) ... ok
test_modbus_finding (test_core.CoreTest.test_modbus_finding) ... ok
test_no_input_mutation (test_core.CoreTest.test_no_input_mutation) ... ok
test_read_not_alerted (test_core.CoreTest.test_read_not_alerted) ... ok
test_reject_invalid_events (test_core.CoreTest.test_reject_invalid_events) ... ok
test_reject_non_synthetic (test_core.CoreTest.test_reject_non_synthetic) ... ok
test_contagens_oficiais_v20 (test_manometro.CatalogoTest.test_contagens_oficiais_v20) ... ok
test_revogado_remapeado (test_manometro.CatalogoTest.test_revogado_remapeado) ... ok
test_tecnica_multitatica (test_manometro.CatalogoTest.test_tecnica_multitatica) ... ok
test_campo_achatado_e_aninhado (test_manometro.DedupTest.test_campo_achatado_e_aninhado) ... ok
test_estado_mais_recente_vence (test_manometro.DedupTest.test_estado_mais_recente_vence) ... ok
test_fanout_de_dispositivos_do_snapshot_vigente (test_manometro.DedupTest.test_fanout_de_dispositivos_do_snapshot_vigente) ... ok
test_baseline_de_configuracao (test_manometro.DemoTest.test_baseline_de_configuracao) ... ok
test_envelope_integro_e_adulteracao (test_manometro.DemoTest.test_envelope_integro_e_adulteracao) ... ok
test_matriz_separa_comportamento (test_manometro.DemoTest.test_matriz_separa_comportamento) ... ok
test_nao_muta_entrada (test_manometro.DemoTest.test_nao_muta_entrada) ... ok
test_numeros_do_caso_demo (test_manometro.DemoTest.test_numeros_do_caso_demo) ... ok
test_periodo_invalido (test_manometro.DemoTest.test_periodo_invalido) ... ok
test_relatorio_html_autocontido (test_manometro.DemoTest.test_relatorio_html_autocontido) ... ok
test_saude_da_coleta (test_manometro.DemoTest.test_saude_da_coleta) ... ok
test_seletor_de_periodo (test_manometro.DemoTest.test_seletor_de_periodo) ... ok
test_rejeita_exportacao_nao_sintetica (test_manometro.TravaSinteticaTest.test_rejeita_exportacao_nao_sintetica) ... ok

----------------------------------------------------------------------
Ran 25 tests in 0.144s

OK
```
