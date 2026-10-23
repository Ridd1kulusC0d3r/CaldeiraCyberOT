"""Leitura defensiva de exportações de documentos (offline).

Formato aceito (o demo usa este):
  {"schema": "caldeira.manometro.synthetic.v1", "synthetic": true,
   "policy": {...}, "docs": [{"_id": ..., "_source": {...}}, ...]}

A trava `synthetic: true` é proposital, igual ao runner do núcleo: o
repositório público só processa dados fictícios. Quem adaptar a ferramenta
para dados reais deve fazê-lo fora deste repositório e sob a política de
dados da própria organização.
"""
import json
from pathlib import Path

ESQUEMA = "caldeira.manometro.synthetic.v1"
LIMITE_BYTES = 25_000_000


def carregar_exportacao(caminho):
    caminho = Path(caminho)
    if caminho.stat().st_size > LIMITE_BYTES:
        raise ValueError("Exportação excede o limite de 25 MB do laboratório.")
    bruto = json.loads(caminho.read_text(encoding="utf-8"))
    if bruto.get("schema") != ESQUEMA or bruto.get("synthetic") is not True:
        raise ValueError("Apenas exportações explicitamente marcadas como sintéticas são aceitas.")
    docs = bruto.get("docs")
    politica = bruto.get("policy", {})
    if not isinstance(docs, list) or not isinstance(politica, dict):
        raise ValueError("Exportação requer docs[] e policy{}.")
    fontes = []
    for i, d in enumerate(docs):
        fonte = d.get("_source", d) if isinstance(d, dict) else None
        if not isinstance(fonte, dict):
            raise ValueError(f"Documento inválido na posição {i}.")
        fontes.append(fonte)
    return {
        "case_id": bruto.get("case_id", "UNSPECIFIED"),
        "generated_by": bruto.get("generated_by"),
        "policy": politica,
        "docs": fontes,
    }
