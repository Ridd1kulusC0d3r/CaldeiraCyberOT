"""CLI do MANÔMETRO (offline).

  python -m manometro analisar manometro/fixtures/demo-xdome.json --de 2026-01 --ate 2026-10 \
      --json saida/manometro.json --html saida/manometro.html
  python -m manometro verificar saida/manometro.json
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from core.evidence import seal, verify

from . import __version__
from .carga import carregar_exportacao
from .kpis import calcular
from .matriz import CATALOGO_PADRAO, carregar

MES = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")


def analisar(caminho, de=None, ate=None, catalogo=CATALOGO_PADRAO):
    for rotulo, valor in (("--de", de), ("--ate", ate)):
        if valor and not MES.match(valor):
            raise ValueError(f"{rotulo} deve estar no formato AAAA-MM.")
    exp = carregar_exportacao(caminho)
    cat = carregar(catalogo)
    kpis = calcular(exp, cat, de, ate)
    payload = {
        "tool": "caldeira.manometro",
        "version": __version__,
        "mode": "OFFLINE_SYNTHETIC_ONLY",
        "case_id": exp["case_id"],
        "input_sha256": hashlib.sha256(Path(caminho).read_bytes()).hexdigest(),
        "attack_ics": {"version": cat["attack_version"], "source_sha256": cat["source_sha256"]},
        "kpis": kpis,
    }
    return seal(payload)


def main(argv=None):
    p = argparse.ArgumentParser(prog="python -m manometro", description="MANÔMETRO: KPIs honestos de OT, offline.")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("analisar", help="calcula KPIs a partir de uma exportação sintética")
    a.add_argument("exportacao")
    a.add_argument("--de", help="mês inicial AAAA-MM (padrão: primeiro mês com dados)")
    a.add_argument("--ate", help="mês final AAAA-MM (padrão: último mês com dados)")
    a.add_argument("--json", help="grava o envelope selado neste arquivo")
    a.add_argument("--html", help="gera o relatório HTML estático neste arquivo")
    v = sub.add_parser("verificar", help="confere o digest SHA-256 de um envelope")
    v.add_argument("envelope")
    args = p.parse_args(argv)

    if args.cmd == "verificar":
        env = json.loads(Path(args.envelope).read_text(encoding="utf-8"))
        ok = verify(env)
        print("ÍNTEGRO: o payload confere com o digest." if ok else "ALTERADO: o payload não confere com o digest.")
        print("Lembrete: SHA-256 mede integridade, não autoria.")
        return 0 if ok else 1

    try:
        env = analisar(args.exportacao, args.de, args.ate)
    except (ValueError, OSError) as erro:
        print(f"ERRO: {erro}", file=sys.stderr)
        return 2
    texto = json.dumps(env, ensure_ascii=False, indent=2, sort_keys=True)
    if args.json:
        Path(args.json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json).write_text(texto + "\n", encoding="utf-8")
    if args.html:
        from .relatorio import renderizar

        Path(args.html).parent.mkdir(parents=True, exist_ok=True)
        Path(args.html).write_text(renderizar(env), encoding="utf-8")
    if not args.json and not args.html:
        print(texto)
    else:
        k = env["payload"]["kpis"]
        print(f"Período {k['periodo']['de']} → {k['periodo']['ate']}: {k['alertas']['no_periodo']} alertas únicos "
              f"({k['coleta']['documentos_alerta']} documentos de alerta no arquivo), "
              f"saúde da coleta: {k['saude']['status']}. Digest {env['digest'][:16]}…")
        for destino in (args.json, args.html):
            if destino:
                print(f"  → {destino}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
