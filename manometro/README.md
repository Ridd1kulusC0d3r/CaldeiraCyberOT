# MANÔMETRO · KPIs honestos de OT

[← Caldeira](../README.md) · [**COMECE AQUI**](COMECE-AQUI.md) · [**Manual ilustrado**](MANUAL.html) · [Relatório de testes](RELATORIO-TESTES.md)

> Uma caldeira se opera pelo manômetro, não pela aparência do tanque. Este braço mede **o que a fonte realmente entrega** antes de virar dashboard.

O MANÔMETRO lê uma exportação de documentos da integração **Claroty xDome → Elastic** e calcula KPIs executivos e operacionais de OT **depois** de três correções que mudam os números, e depois enriquece com inteligência de ameaças:

1. **Deduplicação.** A integração re-consulta a API e regrava o estado dos alertas, e cada alerta vira um documento por dispositivo afetado. Agrupamos por `claroty_xdome.alert.id` e ficamos com o estado do maior `updated_time`. No caso demo, **707 documentos de alerta são 19 alertas** (fator 37×).
2. **Normalização ATT&CK for ICS v20.0.** O catálogo é derivado do STIX oficial da MITRE (12 táticas · 78 técnicas · 26 subtécnicas). IDs revogados viram o substituto oficial (`T0855 → T1692.001`, `T0857 → T1693.001`, `T0812 → T1694.001`) e IDs de outro domínio no campo de ICS (ex.: `T1059`) ficam fora da cobertura.
3. **Comportamento × exposição.** Alerta de postura (categoria `Risk`: SMBv1, firmware antigo, certificado vencido) não é adversário. A matriz mostra os dois e filtra cada um.

4. **Grafo de atores e campanhas.** As técnicas dos alertas de comportamento são cruzadas com os 14 grupos, 10 campanhas e 25 softwares do ATT&CK for ICS v20.0 (relações `uses` e `attributed-to` do STIX oficial). Grupos herdam as técnicas das campanhas atribuídas a eles, e cada campanha aponta para o caso correspondente do [atlas do Caldeira](../docs/casos-ot/README.md). Sai como grafo interativo no relatório, ranking e arquivo **GraphML** (Gephi, yEd, Maltego, Neo4j). **Sobreposição de técnicas não é atribuição**: é hipótese de caça.

Junto vêm exposição de ativos (fim de vida, firmware, protocolo legado por nível Purdue), **Configuration Download** origem → destino contra baseline e **saúde da coleta**. A saída é um envelope JSON com SHA-256 (via [`core/evidence.py`](../core/evidence.py)) e um relatório HTML estático PT/EN, claro/escuro/sistema, na identidade visual v3 do Caldeira (família LLMInjection, ver [BRAND.md](../assets/brand/BRAND.md)).

> [!IMPORTANT]
> **Escopo do repositório público:** somente dados sintéticos (`"synthetic": true`), offline, sem sockets, sem conexão com Elastic, API do fornecedor ou ativos OT. O mapeamento ATT&CK é do fornecedor e **não prova execução** da técnica.

## Rodar em 1 minuto

```bash
python -m manometro analisar manometro/fixtures/demo-xdome.json --de 2026-01 --ate 2026-10 \
    --json saida/manometro-demo.json --html saida/manometro-demo.html --graphml saida/manometro-demo.graphml
python -m manometro verificar saida/manometro-demo.json
```

Sem terminal: dois cliques no lançador do seu sistema em [`lancadores/`](lancadores/).

## O que o caso demo esconde (para você encontrar)

| Achado | Onde aparece |
|---|---|
| 707 documentos → 19 alertas únicos | Card 1 e recomendação 2 |
| Somar `devices_count` por alerta dá 130; dispositivos distintos são 80 | Card 3 |
| 13 técnicas com alerta mapeado, só 8 com comportamento; táticas 9 → 7 | Matriz, filtro *Comportamento* |
| `T0855`, `T0857`, `T0812` revogados no v20.0; `T1059` fora do ICS | Qualidade do mapeamento |
| SMBv1 em níveis Purdue 2 e 3 | Exposição de ativos |
| `PC-17 → PLC-04` (estação de TI) e `SCADA-02 → HMI-07` fora do baseline | Configuration Download |
| HTTP 401/429 e JSON truncado na coleta | Banner + Saúde da coleta |
| INCONTROLLER cobre as 8 técnicas de comportamento; Sandworm aparece via campanhas de 2015 e 2022 | Atores, campanhas e software |

## Estrutura

| Arquivo | Papel |
|---|---|
| [`campos.py`](campos.py) | **Único** mapa de nomes de campo, com status `doc` / `ecs` / `suposto` |
| [`carga.py`](carga.py) | Trava sintética e limites de entrada |
| [`dedup.py`](dedup.py) | Estado vigente por alerta e fan-out de dispositivos |
| [`matriz.py`](matriz.py) | Deriva o catálogo do STIX oficial; normaliza IDs |
| [`grafo.py`](grafo.py) | Deriva o grafo grupos/campanhas/software; cruza com os alertas; exporta GraphML |
| [`kpis.py`](kpis.py) | KPIs, período, natureza, recomendações |
| [`relatorio.py`](relatorio.py) | HTML estático autocontido |
| [`gerar_demo.py`](gerar_demo.py) | Caso demo determinístico (IPs RFC 5737) |
| [`dados/attack-ics-v20.0.json`](dados/attack-ics-v20.0.json) | Catálogo derivado + SHA-256 da fonte |
| [`dados/attack-ics-v20.0-grafo.json`](dados/attack-ics-v20.0-grafo.json) | Grafo derivado (334 arestas) + SHA-256 da fonte |
| [`../tests/test_manometro.py`](../tests/test_manometro.py) | 23 testes offline |

## Política (no próprio arquivo de entrada)

`status_resolvido`, `categorias_exposicao`, `categoria_dispositivo`, `eol_estados`, `tipos_firmware_desatualizado`, `tipos_protocolo_legado`, `niveis_purdue_atencao`, `tipos_evento_config`, `baseline_config`, `grafo_natureza` (`comportamento` ou `todas`) e `grafo_limite`. Valores padrão em [`kpis.py`](kpis.py). Eles variam por ambiente: confirme os valores reais de `category`, `status` e `event.type` no seu índice.

## Limites conhecidos

- `claroty_xdome.event.source.device.name` e `...destination.device.name` não constam da referência pública da integração; o relatório avisa no rodapé.
- A referência da integração mostra *Configuration Upload* como exemplo de `event.type`. Confirme com o fornecedor o sentido de *download*/*upload* no seu ambiente antes de tratar como escrita no controlador.
- Técnica que pertence a várias táticas conta em todas (é como a matriz funciona); por isso “táticas com alerta” é indicador de leitura, não de severidade.

## Fontes

- [Referência da integração Elastic Claroty xDome](https://www.elastic.co/docs/reference/integrations/claroty_xdome)
- [MITRE ATT&CK for ICS · STIX oficial (attack-stix-data)](https://github.com/mitre-attack/attack-stix-data)
- [Termos de uso do ATT&CK](https://attack.mitre.org/resources/legal-and-branding/terms-of-use/)

<sub>MITRE ATT&CK® é marca registrada de The MITRE Corporation. Projeto independente, sem afiliação com MITRE, Claroty ou Elastic.</sub>
