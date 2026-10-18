# Matriz imparcial para avaliar soluções de defesa OT

**CALDEIRA / VENDOR ASSESSMENT** · documento didático, não ranking. Nenhuma pontuação real foi atribuída aos fornecedores.

## Como evitar escolhas por propaganda

Use **exigências do processo industrial** para construir critérios e evidências de aceitação. Qualquer solução que exija intervenção no ambiente deve passar por avaliação de segurança de processo antes de teste ou contratação.

| Critério | Pergunta de verificação | Evidência | Nota |
|---|---|---|---|
| **Compatibilidade OT** | Reconhece ativos, firmwares e protocolos relevantes à instalação? | Matriz oficial + validação autorizada | 0–3 |
| **Método de descoberta** | Coleta passiva, ativa, agentes, sensores embarcados ou modo híbrido? | Guia de arquitetura e limitação declarada | 0–3 |
| **Segurança operacional** | Há plano documentado de risco, regressão e contingência? | Validação conjunta com engenharia e fornecedor | 0–3 |
| **Qualidade da detecção** | Cobertura observável, rastreabilidade, precisão e tuning? | Relatório de teste reproduzível | 0–3 |
| **Integração** | Exporta eventos e contexto com rastreabilidade? | Documentação API / SIEM / formato | 0–3 |
| **Governança** | Menor privilégio, revisão de políticas, dados e retenção? | Matriz RBAC e trilhas de auditoria | 0–3 |
| **Ciclo de vida** | Requisitos de atualização, suporte a legado, licenciamento? | Matriz de suporte e contrato | 0–3 |
| **Independência de fornecedor** | Dados são exportáveis? Existem dependências fechadas? | Teste de portabilidade e documentação | 0–3 |

**Escala didática:** 0 = não demonstrado; 1 = apenas afirmação comercial; 2 = documentação técnica verificável; 3 = comprovação independente **no contexto autorizado**. **Sem evidência, não pontuar 3.** Não somar notas como se fossem decisão automática: segurança de processo pode ser condição impeditiva.

## Questões específicas por perfil

- **Dragos / Nozomi / Claroty:** quais observáveis e evidências sobre o processo justificam os alertas, além de um IOC?
- **Fortinet / Cisco:** como as políticas de segmentação interagem com dependências e exceções aprovadas?
- **Armis / Tenable OT:** que inferências sobre exposição estão vinculadas à criticidade operacional e à completude do inventário?
- **TXOne:** que modos de prevenção ou inspeção são compatíveis com legado, e como controlar risco de falso positivo?

Estas perguntas servem para **estudo comparativo**, não para executar testes ativos em redes industriais reais. Não incluir alvos, credenciais ou configurações sensíveis em resultados públicos.

## Exemplo de interpretação

Um produto pode ter excelente visibilidade documentada e ainda não ser adequado a determinada planta pela janela de manutenção, requisitos de safety, arquitetura, suporte do fabricante e recursos locais. A decisão final exige validação com OT, operações e gestão de riscos.

**Fontes:** [fornecedores do Caldeira](fornecedores.md) · [ISA/IEC 62443](https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards) · [NIST 800-82 Rev.3](https://csrc.nist.gov/pubs/sp/800/82/r3/final).
