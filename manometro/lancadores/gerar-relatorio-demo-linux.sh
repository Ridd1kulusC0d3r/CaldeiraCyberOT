#!/usr/bin/env sh
# MANÔMETRO · lançador de dois cliques (Linux). Gera o relatório do caso demo e abre no navegador.
cd "$(dirname "$0")/../.." || exit 1
PY="$(command -v python3 || command -v python)"
if [ -z "$PY" ]; then
  echo "Python 3.10+ não encontrado. Veja manometro/MANUAL.html > Instalação > Linux."
  printf "Pressione Enter para fechar..."; read _; exit 1
fi
"$PY" -m manometro analisar manometro/fixtures/demo-xdome.json --de 2026-01 --ate 2026-10 \
  --json saida/manometro-demo.json --html saida/manometro-demo.html || { printf "Falhou. Enter para fechar..."; read _; exit 1; }
xdg-open saida/manometro-demo.html >/dev/null 2>&1 || echo "Abra no navegador: $(pwd)/saida/manometro-demo.html"
