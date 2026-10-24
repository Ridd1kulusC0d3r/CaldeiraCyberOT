# COMECE AQUI · MANÔMETRO

[← README do braço](README.md) · [Manual ilustrado](MANUAL.html)

Uma ação por vez. Marque e siga.

- [ ] **1. Tenha Python 3.10+.** Teste: `python3 --version` (Windows: `py -3 --version`). Não há pacotes para instalar.
- [ ] **2. Rode o lançador do seu sistema** em [`lancadores/`](lancadores/):
  - Windows → `gerar-relatorio-demo-windows.bat`
  - macOS → `gerar-relatorio-demo-macos.command` (botão direito → Abrir, na 1ª vez)
  - Linux → `gerar-relatorio-demo-linux.sh`
- [ ] **3. Leia o banner laranja** no topo do relatório. Saúde da coleta vem antes de qualquer número.
- [ ] **4. Compare o card 1:** 17 alertas × 707 documentos.
- [ ] **5. Na matriz, clique em “Comportamento”.** Táticas 9 → 7.
- [ ] **6. Ache `T0855 → T1692.001`** em *Qualidade do mapeamento*.
- [ ] **7. Ache a linha vermelha `PC-17 → PLC-04`** em *Configuration Download*.
- [ ] **8. No grafo de atores, passe o mouse em “Remote System Discovery”.** Hipótese de caça, não atribuição.
- [ ] **9. Abra `saida/manometro-demo.graphml` no Gephi ou yEd** (opcional).
- [ ] **10. Verifique a integridade:** `python3 -m manometro verificar saida/manometro-demo.json` → **ÍNTEGRO**.

Prefere terminal? Da raiz do repositório:

```bash
python3 -m manometro analisar manometro/fixtures/demo-xdome.json --de 2026-01 --ate 2026-10 \
    --json saida/manometro-demo.json --html saida/manometro-demo.html --graphml saida/manometro-demo.graphml
python3 -m unittest discover -s tests -v
```

**Safety:** dados fictícios, offline. Nada aqui serve para decisão automática em processo físico.
