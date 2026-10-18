# Portal de pesquisa · GitHub Pages

Um frontend estático, responsivo e navegável está em [`docs/index.html`](index.html).

## Publicação opcional

Como o GitHub Pages precisa ser ativado nas configurações do repositório, **a publicação pública do portal não está confirmada**. O arquivo HTML já está versionado.

1. Abra **Settings → Pages** no repositório.
2. Em **Build and deployment**, selecione **Deploy from a branch**.
3. Escolha **main**, pasta **/docs**, e salve.
4. Aguarde o deploy indicado pelo próprio GitHub e confira o endereço informado em Pages.

## Recursos existentes

- Layout original Caldeira, com grade de telemetria e radar industrial.
- Navegação por domínios, busca de texto e filtros de conteúdo.
- Indicadores Fortinet 2026 com ressalva sobre amostra e fonte.
- Cards de fontes primárias e atalhos diretos para documentação GitHub.
- Responsividade mobile, navegação por teclado, foco visível e redução de animações quando solicitada.
- Sem dependências externas, rastreamento ou APIs.

## Limites

O site é um catálogo editorial e **não um dashboard de telemetria em tempo real**. Valores exibidos são estáticos e exigem curadoria para atualização. Nenhum dado é extraído automaticamente de redes industriais.

**Manutenção:** sempre que adicionar nova seção, inclua o link equivalente no arquivo HTML e no README principal.