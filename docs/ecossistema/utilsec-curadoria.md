# 12 / UtilSec · curadoria crítica de referências OT (18/10/2026)

**Escopo autorizado:** somente os dez repositórios utilsec selecionados pelo mantenedor do Caldeira. **Não** importar código, capturas, infográficos, PDFs ou DOCX; **não** instalar nem executar ferramentas; **não** alterar o projeto Mininet.

**Resultado:** cinco referências de estudo aprovadas, duas referências condicionadas e três entradas mantidas em triagem. **Referência aprovada** significa que seu *propósito documental* se encaixa no Caldeira, não que o conteúdo, seus dados ou seus resultados tenham sido integralmente auditados.

[Voltar ao catálogo externo](repositorios-e-projetos.md) · [Metodologia e proveniência](../metodologia-cti-ot.md) · [Catálogo estruturado](../../catalogo/fontes-utilsec.json)

## A / Referências de estudo aprovadas

| Projeto | Contribuição original ao Caldeira | Avaliação e limites |
|---|---|---|
| **[ot-threat-dashboard](https://github.com/utilsec/ot-threat-dashboard)** | Feed editorial de inteligência OT/ICS com formatos JSON/RSS e recortes setoriais (energia, água, manufatura, transporte, óleo e gás e outros). | **5/5.** Referência de *descoberta de pautas*, nunca fonte primária automática. Conferir advisories, CVEs, atribuições, datas e severidade na origem de cada notícia. |
| **[examine_pcap](https://github.com/utilsec/examine_pcap)** | Exemplo de leitura **offline** de capturas para investigação de inventário Modbus TCP. | **4/5.** A implementação observada identifica candidatos a servidor pelo **TCP de origem 502**, sem comprovar conteúdo Modbus. MAC/OUI pode refletir equipamento intermediário ou virtual. Não tratar o resultado como inventário validado. |
| **[Getting_Started_with_ICS](https://github.com/utilsec/Getting_Started_with_ICS)** | Dois livros introdutórios, um orientado a profissionais de TI e outro a profissionais OT. | **4/5.** Já constava no catálogo Caldeira. Preservar **uma** referência canônica, sem republicar os PDFs. A inspeção cobriu o inventário dos arquivos, não a íntegra dos livros. |
| **[ICS_OT_Intro_Course_Resources](https://github.com/utilsec/ICS_OT_Intro_Course_Resources)** | Plano de curso e questões de revisão em DOCX, além de quatro guias rápidos em PDF. | **4/5.** Referência de percurso educacional, não orientação para varrer redes industriais reais. Conteúdo integral dos arquivos binários não foi auditado. |
| **[Infographics](https://github.com/utilsec/Infographics)** | Referências visuais sobre maturidade, competências e gestão de vulnerabilidades OT. | **3/5.** Apenas links e temas; números e claims de figuras devem ser rastreados até fontes técnicas. Não duplicar imagens de terceiros. |

### Feed OT: como interpretar a proveniência

O arquivo [feed.json](https://github.com/utilsec/ot-threat-dashboard/blob/main/feed.json) declara autoria editorial de **Mike Holcomb**, parceria com **UtilSec**, links para as fontes das notícias e orientação de reutilização com crédito. Na inspeção de **18/10/2026**, o feed geral mostrava geração em **2026-10-18T06:10:00-04:00**; feeds setoriais consultados tinham atualizações anteriores. Esses horários descrevem o conteúdo observado, **não** um pipeline implementado no Caldeira.

O feed não estabelece, sozinho, que um incidente ocorreu, que uma CVE foi explorada ou que uma empresa sofreu impacto físico. Registrar o **link primário do item**, a origem da afirmação, a data do acontecimento e o nível de confiança; não copiar resumos em massa. A declaração de atribuição em um feed **não** substitui licença explícita para reutilização de todo o código ou toda a base.

### Inventário por PCAP: limite técnico

O código de `examine_pcap` usa a **porta de origem TCP/502** como filtro, IP/MAC da origem e consulta OUI. Isso é útil como hipótese de inventário, mas não verifica handshake de aplicação, função Modbus, roteamento, identidade do PLC nem integridade do dataset. A alegação do README de identificação garantida de equipamento Modbus não se sustenta apenas nesse filtro. Preferir documentação de como *validar resultados* a replicação de código.

## B / Referências com ressalvas ou redundância

| Projeto | Decisão | Justificativa |
|---|---|---|
| **[QuickStart-Guides](https://github.com/utilsec/QuickStart-Guides)** | **Referência cruzada, não novo conteúdo canônico.** | Os quatro PDFs **Nmap** e **Shodan** possuem os mesmos hashes Git de arquivos homônimos em `ICS_OT_Intro_Course_Resources`: não é só assunto parecido, é duplicação binária na revisão de 18/10/2026. Evitar listar como quatro documentos inéditos. |
| **[CompTIA-SecOT-Exam-Sim](https://github.com/utilsec/CompTIA-SecOT-Exam-Sim)** | **Referência educacional não oficial e condicionada.** | O HTML inspecionado exibe `SecOT+ Study Console — SOT-001` e declara no rodapé que é auxílio independente, **não afiliado nem endossado pela CompTIA**. Não apresentar como material oficial, comprovação de certificação válida ou currículo homologado. O DOCX associado não foi auditado na íntegra. |

### Evidência da duplicação

Comparação dos Git blob SHA-1 do mesmo nome em `ICS_OT_Intro_Course_Resources` e `QuickStart-Guides`:

| Arquivo PDF nos dois repositórios | Blob SHA-1 idêntico |
|---|---|
| Nmap QuickStart Guide for ICS OT.pdf | `99b2a61fbc6836ea2bee8422771749467e1cb5c3` |
| Nmap QuickStart Guide.pdf | `ebd326045879c082d4549489525e9623e4414714` |
| Shodan QuickStart Guide for ICS OT.pdf | `85aaaebe6bca7eeddede7ff710c59a5a8aa17678` |
| Shodan QuickStart Guide.pdf | `b486c2308ca9fadf4b9bd1ffafaff9af12db45e8` |

*Nota:* hashes Git de blobs são identificadores de conteúdo no repositório, não checksums publicados de proveniência editorial dos autores.

## C / Em triagem: não promover a fonte até resolver pendências

| Projeto solicitado | Observação verificável | Pendência e limite |
|---|---|---|
| **atomics** | README descreve ferramenta de avaliação ICS, inventário e protocolos, mas também capacidades ativas com potencial de alteração de estado industrial. | **Não endossar nem incorporar ferramenta operacional** em base documental; somente uma análise futura de seus *conceitos passivos* e riscos, separada de instruções de uso. |
| **[ChatGPT_for_ICS_OT](https://github.com/utilsec/ChatGPT_for_ICS_OT)** | README contém apenas o título e há um manual de laboratório `.docx` de 792.441 bytes (Git tree). | Não foi possível auditar o conteúdo integral do DOCX: **não avaliar como guia de IA responsável, atualizado ou tecnicamente correto** até revisão do documento. |
| **[OT-ICS-Packet-Captures](https://github.com/utilsec/OT-ICS-Packet-Captures)** | Um único arquivo `pentest_001.pcap`, 8.619 bytes; não há README ou ficha de dataset no inventário observado. | **Não catalogar como dataset validado** sem autoria, captura autorizada, protocolo, ambiente, janela temporal, anonimização, rótulos e direitos de distribuição. Não baixamos, abrimos ou espelhamos o PCAP. |

## D / Proveniência, licença e status de revisão

- **Publicador aparente:** conta GitHub `utilsec`; nos materiais editoriais examinados, há referência nominal a **Mike Holcomb**. Não deduzir que a conta é autora exclusiva de cada arquivo.
- **Consulta de metadados:** em **18/10/2026**, nenhum dos **dez** repositórios selecionados declarou licença reconhecida (`license.spdx_id`) pela API consultada; as árvores de arquivos inspecionadas também não exibiam `LICENSE` na raiz. **Ausência de licença declarada não é licença livre.** A política permanece *somente citar e apontar para a fonte*.
- **Binários:** PDFs, DOCX, figuras e PCAP **não** foram espelhados, incorporados nem submetidos a uma auditoria integral. A presença de arquivos no Git **não** valida o conteúdo.
- **Coleta:** metadados de repositórios, README e árvores Git; código textual lido apenas para observar limitações do `examine_pcap` e o rodapé do HTML educacional. Não houve execução em rede OT.
- **Revisões futuras:** mudanças em permissões, termos, suporte ou conteúdo devem resultar em revisão desta ficha. Datas `pushed_at` do GitHub representam alteração do repositório, **não** validação editorial de fatos.
- **Classificação:** aprovado = adequado para referência temática; condicionado = útil sob ressalvas; em triagem = sem evidência suficiente para recomendar como fonte validada.

## E / Fronteira entre Caldeira e Mininet

Este documento não adiciona dependências ou integrações de execução. **Caldeira = evidência, pesquisa e raciocínio defensivo. Mininet = projeto independente de emulação.** Nenhuma dessas fontes justifica comando sobre instalações industriais reais.

*Revisado em 18 de outubro de 2026; inventário baseado nos caminhos e metadados presentes nos repositórios nessa data.*
