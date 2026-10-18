# Fortinet · State of Operational Technology and Cybersecurity · 2026

**Tipo:** relatório anual · **idioma do anexo:** PT-BR · **extensão:** 19 páginas · **autor/publicador:** Fortinet · **consulta:** 18/10/2026.

**Documento fonte:** [Fortinet — 2026 State of Operational Technology and Cybersecurity Report](https://www.fortinet.com/resources/reports/state-ot-cybersecurity).

> **Transparência:** esta página contém síntese e crítica **originais** da edição PDF fornecida para estudo; os dados percentuais abaixo são reproduzidos pontualmente com páginas de referência. Não é uma reprodução integral do relatório.

## 1. Metodologia e limites da amostra

Na **página 7**, a Fortinet apresenta a oitava edição da pesquisa, baseada em **mais de 700 profissionais ligados a OT**. Nas **páginas 16–18**, informa que a pesquisa foi conduzida pela empresa independente **Empanel Online**, com responsáveis de gestão e liderança de **organizações com mais de 1.000 funcionários**, sobretudo manufatura e energia, distribuídas por diversas regiões.

**Limites para interpretação:** amostra e perguntas representam percepções declaradas pelos respondentes, não auditorias diretas de todos os ativos. O relatório é publicado por fornecedor com oferta comercial no domínio. É inadequado generalizar as estimativas para toda a infraestrutura mundial, pequenas empresas ou um país específico sem ressalva.

## 2. Evidências extraídas

| Tema | Achado do PDF | Página | Leitura analítica |
|---|---|---:|---|
| **Governança** | 60% atribuem responsabilidade final ao CISO/CIO; 81% dos respondentes informam intenção de transferência ao CISO nos 12 meses seguintes, nos termos do questionário. | **3** | A governança está em transformação; não confundir intenção e implementação. |
| **Processos** | Declarações de maturidade de processos em nível 4 caíram de 49% (2025) para 17% (2026). | **4** | Autoavaliação pode mudar com maior consciência dos riscos; não provar regressão operacional. |
| **Incidentes** | 71% relataram **1 a 9 invasões** no último ano; relatório menciona 47% no comparativo anterior. | **5** | Mudanças na detecção e na propensão a reportar podem afetar números. |
| **Expectativa regulatória** | 89% esperam aumento das regulamentações em até cinco anos, contra 66% em 2025. | **6** | Expectativas, e não contagem de normas efetivamente publicadas. |
| **Tempo de permanência** | Categoria **semanas**: 13% (2026); categoria **meses**: 7% (2026) no gráfico comparativo. | **9** | Requer conhecer o método de medição de dwell time; não é mediana de tempo. |
| **Visibilidade OT** | 14% relatam visibilidade de **100%** dos sistemas; 23% relatam visibilidade de cerca de metade. | **9** | Uma declaração de cobertura não substitui teste de completude de inventário. |
| **Ambientes impactados** | 24% informaram que **ambos**, TI e OT, foram afetados por invasões, ante 60% em 2025. | **10** | O PDF sugere segmentação como hipótese; a pergunta não estabelece causalidade. |
| **Tipos de intrusão** | Phishing: 76%; ransomware/wiper: 50% (edição 2026). | **11** | Refere-se a tipos declarados de invasão; não equivale a taxa de vítimas no mercado. |
| **Impacto operacional** | 46% relataram interrupção operacional com impacto na receita, frente a 42% em 2025; perda de dados críticos: 44%. | **12** | Impacto autorrelatado entre entrevistados, sem inferir dano financeiro agregado. |
| **Modernização** | 40% relataram sistemas ICS com menos de cinco anos (20% em 2025). | **12** | Comparação dependente de composição de amostra e respostas. |

## 3. Interpretação independente · Caldeira

**Visibilidade ≠ proteção.** O aumento de autopercepção de inventário não mede automaticamente detecção de técnicas ICS. Uma análise defensiva deve observar: cobertura real de redes, mudanças em baseline, processos com maior impacto, integridade dos ativos e validação por operadores.

**Maturidade autoavaliada ≠ conformidade certificada.** A queda do nível 4 percebido pode significar reclassificação e maior exigência, hipótese apresentada pelo próprio relatório. O questionário não permite distinguir plenamente as explicações.

**Volume relatado ≠ volume real de intrusões.** Melhor detecção ou diferença de participantes pode elevar contagens relatadas. Por isso a série deve ser analisada com cautela.

**Causalidade não estabelecida.** A redução da proporção de incidentes simultâneos TI/OT é compatível com segmentação, mas o levantamento não isola o efeito de segmentar redes.

**A edição 2025 não é a edição 2026.** O [blog de 2025](https://www.fortinet.com/br/blog/business-and-technology/key-findings-from-the-fortinet-2025-operational-technology-security-report) é referência histórica separada, não substitui a coleta e o PDF de 2026.

## 4. Cinco áreas de recomendação apresentadas no relatório

As recomendações das **páginas 15–16** são: (1) segmentação e microssegmentação entre TI e OT; (2) acesso remoto seguro; (3) integração da OT às operações de segurança e planos de resposta a incidentes; (4) inteligência de ameaças específica de OT; (5) simplificação da arquitetura por plataformas integradas.

**Crítica importante:** essa quinta área corresponde também ao posicionamento comercial do publicador. Validar plataformas versus soluções interoperáveis considerando segurança de processo, cobertura, dependência de fornecedor, custos, operação e continuidade. Uma arquitetura integradora não é automaticamente superior para toda planta.

## 5. Aplicação defensiva no Caldeira

| Evidência do relatório | Questão a examinar na planta ou laboratório | Artefato |
|---|---|---|
| Parcela com inventário incompleto | Quais ativos aparecem em fontes autorizadas e no tráfego passivo? | Matriz de cobertura |
| Dwell time em semanas/meses | Qual telemetria indicaria atividade anômala não percebida? | Hipóteses de detecção |
| Impacto nas operações | Quais dependências de TI são essenciais à produção? | Mapa de dependências |
| Mudança de governança | Quem pode autorizar contenção, restauração e isolamento? | RACI de resposta |
| Exposição a terceiros | Como controlar sessões, privilégios e registro de acesso? | Checklist de acesso remoto |

### Referências e proveniência

- **Fonte primária da análise:** anexo fornecido para estudo, *Relatório 2026 sobre o Estado da Tecnologia Operacional e Cibersegurança*, Fortinet, 19 pp., páginas citadas na tabela.
- **Página oficial 2026:** https://www.fortinet.com/resources/reports/state-ot-cybersecurity
- **Histórico 2025:** https://www.fortinet.com/br/blog/business-and-technology/key-findings-from-the-fortinet-2025-operational-technology-security-report
- **Data de revisão editorial:** 18/10/2026.

**Direitos:** PDF integral e elementos gráficos pertencem ao respectivo titular; distribuição original deve ocorrer pelos canais autorizados.