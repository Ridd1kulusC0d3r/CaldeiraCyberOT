# 09 / Datasets e evidências para pesquisa Cyber OT

A base científica precisa diferenciar **tráfego de rede**, **séries temporais de processo**, **eventos de host** e **casos históricos reconstruídos**. Misturar esses materiais em um único benchmark sem proveniência produz conclusões frágeis.

## Fontes priorizadas

| Fonte | Mantenedor e URL | Modalidade | Aplicação válida | Limitação |
|---|---|---|---|---|
| **CyOTE Insights** | [Idaho National Laboratory](https://cyote.inl.gov/tools/cyote-insights/) · [GitHub](https://github.com/idaholab/Insights) | Precursor Analysis Reports, observáveis e comparações entre casos | Hipóteses de CTI e linha do tempo de campanhas | Reconstrução de fontes públicas não equivale a captura completa do incidente |
| **Cyber4OT** | [Cabaj et al. / repositório](https://github.com/krzysztof-cabaj/Cyber4OT) · [artigo](https://doi.org/10.1016/j.softx.2025.102196) | **96 traces / >4,25 milhões de pacotes** em testbed ICS | Taxonomia de fluxo Modbus, exemplos de telemetria, pesquisa de detecção | Capturas de **experimento com ataque simulado**, não PCAP de uma invasão real |
| **HAI** | [icsdataset/hai](https://github.com/icsdataset/hai) | Dados de processo em infraestrutura HIL | Modelagem de anomalia física e correlações temporais | Variáveis de processo não equivalem a logs de rede; observar termos dos dados |
| **SWaT** | [SUTD iTrust](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/) | Tratamento de água em testbed | Estudo de sensores, atuadores e condições de processo | Download pode exigir solicitação/autorização |
| **WADI** | [SUTD iTrust](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/) | Distribuição de água em testbed | Transferibilidade de modelos de anomalia | Condições e acesso definidos pelo detentor |
| **BATADAL** | [Dados oficiais](https://www.batadal.net/data.html) | Séries temporais de distribuição de água | Benchmark de detecção de processo | Não assumir PCAP industrial disponível |
| **ToN_IoT** | [UNSW](https://research.unsw.edu.au/projects/toniot-datasets) | Telemetria IoT/IIoT, rede e logs de sistemas | Stress e validação de pipelines multimodais | IIoT amplo não é representativo de todo ICS |
| **ICSNPP** | [CISA / GitHub](https://github.com/cisagov/ICSNPP) | Código de parser e exemplos de logs industriais | Dicionário de campos observáveis / normalização | É coleção de parsers, **não dataset de incidente** |

## Distinção metodológica

~~~mermaid
flowchart TB
    A["Relatório de incidente"] --> I["Contexto / evidência humana"]
    B["PCAP de testbed"] --> N["Fluxos / protocolos / sessões"]
    C["Série temporal de processo"] --> P["Sensores / atuadores / dinâmica"]
    D["Logs de aplicação / engenharia"] --> L["Autenticação / mudança / auditoria"]
    I --> T["Linha do tempo fundamentada"]
    N --> T
    P --> T
    L --> T
    T --> V["Hipótese defensiva + limites explícitos"]
~~~

**Regras científicas:** preservar particionamento temporal, evitar vazamento entre treino e teste, registrar janela de coleta, relógio/timezone, classes desbalanceadas, versão do dataset, condições da planta e alteração de rótulos. Nunca afirmar que uma detecção de processo prova identificação do tráfego que causou a anomalia.

## Avaliação de qualidade antes de citar

- Documentação do ambiente e origem: testbed, HIL, captura corporativa ou relato histórico.
- Formato e rotulagem: PCAP, CSV, logs, relatório, marcações temporais e verdade-terreno.
- Cobertura e representatividade: protocolos, número de cenários, tempo e setores.
- Integridade e reprodução: versão exata, DOI, checksum e disponibilidade da licença.
- Ética e propriedade intelectual: não espelhar material indisponível para redistribuição.

## Pendentes de validação individual

Os nomes **ICSCASD-MPLC**, **SIMPLE-ICS**, **Electra** e **Power System Attack Dataset** aparecem em materiais de pesquisa, mas **não foram integrados ao catálogo principal** sem confirmação suficiente de origem, DOI, versão, licenciamento e formato. Use como fila de investigação, não como evidência aprovada.

## Catálogo computável

Os incidentes aprovados aparecem em [catalogo/casos.json](../catalogo/casos.json). Datasets não são espelhados. Metadados e links devem ser revisados periodicamente.
