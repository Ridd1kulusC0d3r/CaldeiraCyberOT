"""Verificação offline de referências internas da curadoria OT.

Não acessa URLs externas, não valida conteúdo remoto e não executa cenários OT.
"""
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = [
    "README.md",
    "docs/index.md",
    "docs/referenciais-ot.md",
    "docs/ecossistema/fornecedores.md",
    "docs/ecossistema/avaliacao-fornecedores.md",
    "docs/ecossistema/instituicoes.md",
    "docs/guias/cisa-mitigacoes-ot.md",
    "docs/arquitetura-labs.md",
    "docs/PORTAL.md",
    "manometro/README.md",
    "manometro/COMECE-AQUI.md",
]
HTML = "docs/index.html"
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
HTML_LINK = re.compile(r'href=["\']([^"\']+)["\']')


def verify():
    failures = []
    checked = 0
    for relative in DOCUMENTS + [HTML]:
        document = ROOT / relative
        if not document.is_file():
            failures.append(f"{relative}: arquivo ausente")
            continue
        body = document.read_text(encoding="utf-8")
        links = HTML_LINK.findall(body) if relative == HTML else MARKDOWN_LINK.findall(body)
        for item in links:
            link = item.strip().split()[0].strip("<>")
            parts = urlsplit(link)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            if parts.path.startswith("/"):
                failures.append(f"{relative}: link absoluto local não resolvido {link}")
                continue
            target = (document.parent / unquote(parts.path)).resolve()
            if not target.is_relative_to(ROOT) or not target.exists():
                failures.append(f"{relative}: link interno inválido {link}")
            checked += 1
    for failure in failures:
        print("ERRO:", failure, file=sys.stderr)
    print(f"Documentos analisados: {len(DOCUMENTS)+1}; caminhos internos verificados: {checked}")
    print("URLs externas NÃO foram consultadas nem validadas.")
    return not failures


if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
