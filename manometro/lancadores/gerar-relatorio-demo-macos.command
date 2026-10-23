#!/usr/bin/env bash
# MANÔMETRO · lançador de dois cliques (macOS). Gera o relatório do caso demo e abre no navegador.
cd "$(dirname "$0")/../.." || exit 1
PY="$(command -v python3 || command -v python)"
if [ -z "$PY" ]; then
  echo "Python 3.10+ não encontrado. Veja manometro/MANUAL.html > Instalação > macOS."
  read -r -p "Pressione Enter para fechar..." _; exit 1
fi
"$PY" -m manometro analisar manometro/fixtures/demo-xdome.json --de 2026-01 --ate 2026-10 \
  --json saida/manometro-demo.json --html saida/manometro-demo.html || { read -r -p "Falhou. Enter para fechar..." _; exit 1; }
open saida/manometro-demo.html
