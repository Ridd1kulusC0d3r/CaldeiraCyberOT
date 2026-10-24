# Caldeira Cyber OT Labs / Identidade visual v3 · mesa do analista

**Marca:** CALDEIRA, subtítulo **CYBER OT LABS**. A partir da v3 o Caldeira pertence à mesma família visual do [LLMInjection](https://ridd1kulusc0d3r.github.io/LLmInjection/): papel, tinta e **uma única cor de sinal**. O nome e a voz continuam do Caldeira; a cor de sinal é o **cobre** (herança da v2), não o vermelho-ferrugem do LLMInjection.

Princípio: parece um caderno de engenharia e um relatório de inteligência impresso, não um painel de SOC. Linhas finas separam blocos; nada de gradientes, brilho, sombras ou cantos arredondados grandes.

## Tokens cromáticos

| Token | Claro (padrão) | Escuro | Uso |
|---|---|---|---|
| `--paper` | `#f3f0e8` | `#131210` | Fundo |
| `--paper-2` | `#ebe7dc` | `#1b1915` | Superfície secundária, hover, blocos de código |
| `--ink` | `#17150f` | `#ece8dd` | Texto principal e réguas fortes |
| `--ink-2` | `#4a463c` | `#b9b4a6` | Texto secundário |
| `--ink-3` | `#68635a` | `#908b7d` | Rótulos, IDs, notas |
| `--rule` | `#cfc9ba` | `#37332b` | Réguas finas |
| `--rule-2` | `#e0dacb` | `#27241e` | Réguas muito finas, trilhos de barras |
| `--signal` | `#9c4a0c` | `#e99754` | **Única cor de destaque**: links ativos, fronteira L3.5, achado, alerta |
| `--signal-ink` | `#ffffff` | `#131210` | Texto sobre `--signal` |

Escala sequencial (calor de matriz, barras), sempre do cobre:

| Passo | Claro | Escuro |
|---|---|---|
| `--seq-0` | `#f6e1cc` | `#3a2a1c` |
| `--seq-1` | `#ecbe92` | `#6b4224` |
| `--seq-2` | `#d8925a` | `#a8662f` |
| `--seq-3` | `#9c4a0c` | `#e99754` |
| `--seq-4` | `#6b3407` | `#f6c394` |

Contraste medido: `--signal` sobre `--paper` 5,4:1 (claro) e 8,0:1 (escuro); `--ink` sobre `--paper` acima de 15:1.

## Tipografia

- **Títulos:** serifa — `Georgia, "Iowan Old Style", "Times New Roman", serif`, peso 700, entrelinha justa. Subtítulos (*dek*) em serifa itálica.
- **Texto:** `system-ui, -apple-system, "Segoe UI", Helvetica, Arial, sans-serif`.
- **Rótulos, IDs, números, navegação:** monoespaçada em **caixa alta com espaçamento** (`letter-spacing:.1em–.14em`, 11–12 px). Métricas grandes também em mono.
- Sem fontes externas: tudo do sistema, funciona offline e no GitHub.

## Linguagem visual

- **Masthead:** linha mono `CALDEIRA / CYBER OT LABS` à esquerda, `TLP:CLEAR` à direita, régua de tinta abaixo.
- **Capa:** [`caldeira-hero.svg`](caldeira-hero.svg) — título em serifa, *dek* em itálico, traço de cobre e um desenho técnico em traço de tinta (vaso de pressão com manômetro). O único elemento em cobre no desenho é o ponteiro e a faixa de leitura.
- **Purdue:** [`purdue-layers.svg`](purdue-layers.svg) — livro-razão (ledger) com réguas; só a fronteira **L3.5** usa o sinal.
- **Radar de pesquisa:** [`research-radar.svg`](research-radar.svg) — seis domínios numerados em mono.
- **Faixa de números:** valores grandes em mono, rótulo em mono caixa alta, separadores verticais finos.
- **Tabelas:** cabeçalho mono caixa alta com régua de tinta; linhas com régua fina; números alinhados à direita.
- **Badges (shields.io):** `style=flat-square`, `labelColor=17150f`, cor `9c4a0c` (sinal) ou `4a463c` (neutro).
- **Tema:** claro por padrão; escuro segue o sistema ou o botão *Tema*.
- **Acessibilidade:** nada comunicado só por cor (formas, rótulos e texto acompanham), foco visível com contorno `--signal`, textos alternativos em todos os SVGs.
- **Política editorial (inalterada):** não chamar documentação planejada de ferramenta funcional. Distinguir fato, hipótese, dataset sintético e opinião.

## Marca de terceiros

Nomes e produtos de fornecedores citados pertencem aos titulares. A família visual é compartilhada apenas entre projetos do mesmo autor (Caldeira e LLMInjection); nenhuma relação de patrocínio com terceiros.
