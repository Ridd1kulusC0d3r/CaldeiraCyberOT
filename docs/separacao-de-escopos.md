# Limites de escopo / Caldeira e Mininet

**Atualização de arquitetura em outubro de 2026:** o Caldeira passou a conter **um núcleo próprio de análise offline**, sem transferir o código do repositório Mininet. Os dois projetos continuam independentes, mas complementares.

~~~mermaid
flowchart LR
  C["CALDEIRA CYBER OT LABS"] --> R["Pesquisa global e relatórios"]
  C --> D["Núcleo offline: detecção + hash de integridade"]
  D --> J["Fixtures sintéticas versionadas"]
  M["MININET / projeto externo"] -. "referência bibliográfica e arquitetural" .-> C
~~~

| Tema | CaldeiraCyberOT | Mininet |
|---|---|---|
| Incidentes globais, fontes, fornecedores, normas | **Sim** | Referências contextuais |
| Eventos sintéticos e regras puras de detecção | **Sim** | Tem seu próprio conjunto de detectores |
| Hash SHA-256 de saídas offline | **Sim** | Projeto independente de evidências |
| Captura ativa, topologias e emulação de rede | **Não** | Repositório distinto |
| Execução de OpenPLC, GRFICS e Conpot | **Não** | Não assumida |
| Perfis ATT&CK/CTI para aprendizado | **Sim**, com fontes | Seus próprios mapeamentos |
| KPIs de OT sobre exportações sintéticas de SIEM ([Manômetro](../manometro/README.md)) | **Sim**, offline | Não |
| Conexão com SIEM, API de fornecedor ou ativo OT | **Não** | Não |

**O Caldeira não copia, importa nem executa automaticamente o Mininet.** A documentação de `sims/` sinaliza backends futuros, não módulos operacionais. Para o laboratório funcional do Caldeira consulte [COMECE-AQUI.md](../COMECE-AQUI.md).
