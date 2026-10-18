# Arquitetura / Cyber OT Labs

## Propósito

Caldeira agora tem **duas camadas complementares**, preservando o atlas de pesquisa que já existia:

- **Research & Intelligence:** casos de incidentes, relatórios, pesquisadores, vendors, padrões e referências.
- **Detection & Evidence:** análise offline de eventos sintéticos, detectores puros, mapeamento criterioso ao ATT&CK for ICS e evidência de integridade.

~~~mermaid
flowchart TD
  R["FONTES PÚBLICAS / FONTES OFICIAIS"] --> CUR["CURADORIA GLOBAL E CTI"]
  J["JSON FICTÍCIO / FIXTURES DE TESTE"] --> N["CONTRATO DE EVENTOS NORMALIZADOS"]
  N --> D["CORE / DETECTORES PUROS"]
  CUR -. "referências verificáveis" .-> I["CATÁLOGO ATT&CK for ICS"]
  D --> F["FINDINGS DEFENSIVOS"]
  I -. "mapeamentos com ressalva" .-> F
  F --> E["EVIDÊNCIA CANÔNICA + SHA-256"]
  E --> REP["RELATÓRIO / REVISÃO HUMANA"]
  M["Mininet independente"] -. "referência, sem importação" .-> J
~~~

## Contrato do evento sintético (versão 1)

```json
{
  "schema": "caldeira.synthetic.v1",
  "synthetic": true,
  "case_id": "CAL-LAB-001",
  "policy": { "modbus_approved_sources": { "PLC-SIM-01": ["HMI-SIM-01"] } },
  "events": [
    {
      "event_id": "EX-1",
      "protocol": "modbus",
      "operation": "read",
      "source": "HMI-SIM-01",
      "target": "PLC-SIM-01",
      "zone_from": "OT",
      "zone_to": "OT"
    }
  ]
}
```

**A versão 1 é intencionalmente limitada.** Nada de parsers de payload real, conexão com CLPs, portas abertas, scanner, replay de pacotes ou controles industriais.

## Purdue como organização didática

![Purdue no Caldeira](../assets/brand/purdue-layers.svg)

O modelo Purdue auxilia a pensar fronteiras e funções, mas não é um inventário obrigatório de níveis, nem garante segurança por si só. A **ISA-95 utiliza o Purdue Reference Model for CIM como referência de integração** entre funções empresariais e controle; isso não significa que a ISA-95 seja uma norma de cibersegurança ou sinônimo do Purdue. Os níveis **L3.5 (DMZ) e L5 (conectividade externa)** do nosso diagrama são convenções didáticas de arquitetura, não níveis universalmente obrigatórios. **Sistemas SIS não devem ser tratados como componentes ordinários da mesma cadeia de controle**, pois requisitos e independência de segurança são específicos.

| Nível | Foco de conhecimento | Estado no Caldeira |
|---|---|---|
| **L4–L5** | Empresas e dependências IT | Desvio de fluxo por metadados fictícios |
| **L3.5** | DMZ industrial e controle de acessos | Matriz entre zonas fictícias |
| **L3** | Operação, serviços e histórico | Topologia didática documentada |
| **L1–L2** | HMI/SCADA e controladores | Detector sobre evento Modbus sintético |
| **L0** | Processo físico | Conceitual, sem simulação física implementada |

## Critérios de engenharia

| Elemento | Contrato | Estado |
|---|---|---|
| Detectores | Funções puras com `event, policy` → `finding|None` | Implementado |
| Evidência | Hash SHA-256 sobre JSON canônico; `verify` | Implementado |
| Runner | Arquivo sintético para relatório textual | Implementado |
| CTI | Referências MITRE atuais com URL oficial | Implementado como catálogo |
| API de plug-ins | Formato de saída imutável/estável com versionamento | Planejado |
| Backends OT reais | Integração com bibliotecas e serviços FOSS | Não implementado |
| Painel de evidências | Visual estático/editorial, não SIEM | Parcial |
| Mininet | Repositório externo, sem cópia | Referenciado |

## Cuidados de integridade

SHA-256 detecta divergência entre conteúdo e digest armazenados **quando o digest de referência é confiável**. Não autentica automaticamente a origem, e ambos podem ser substituídos por quem controla os arquivos. Para cadeia de custódia real seriam necessários proveniência, assinatura e registros protegidos.

## Limites de atribuição

Uma detecção de política não é automaticamente uma técnica ATT&CK observada. O código só usa a técnica `T1692.001` como **hipótese analítica**, a ser corroborada por dispositivo, fonte, horário, função e autorização. O detector de fronteira IT→OT evita atribuir técnica na ausência de evidências suficientes.

Referências: [MITRE ATT&CK for ICS](https://attack.mitre.org/matrices/ics/) · [NIST SP 800-82 Rev.3](https://csrc.nist.gov/pubs/sp/800/82/r3/final).

## Complementos normativos

A hierarquia ilustrativa não substitui análise de zonas/conduítes em [ISA/IEC 62443](referenciais-ot.md), nem o guia [NIST SP 800-82](https://csrc.nist.gov/pubs/sp/800/82/r3/final). Para discussão de fronteiras, autenticação e continuidade, consulte as [cinco mitigações prioritárias CISA (2025)](guias/cisa-mitigacoes-ot.md).
