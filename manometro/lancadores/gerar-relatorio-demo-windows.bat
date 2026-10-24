@echo off
rem MANOMETRO - lancador de dois cliques (Windows). Gera o relatorio do caso demo e abre no navegador.
chcp 65001 >nul
cd /d "%~dp0..\.."
set PY=
where py >nul 2>nul && set PY=py -3
if not defined PY where python >nul 2>nul && set PY=python
if not defined PY (
  echo Python 3.10+ nao encontrado. Veja manometro\MANUAL.html ^> Instalacao ^> Windows.
  pause
  exit /b 1
)
%PY% -m manometro analisar manometro\fixtures\demo-xdome.json --de 2026-01 --ate 2026-10 --json saida\manometro-demo.json --html saida\manometro-demo.html --graphml saida\manometro-demo.graphml
if errorlevel 1 (
  pause
  exit /b 1
)
start "" "saida\manometro-demo.html"
