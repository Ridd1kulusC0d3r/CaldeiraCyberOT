"""MANÔMETRO — braço de métricas honestas de OT do Caldeira Cyber OT Labs.

Lê exportações (sintéticas, no demo) de documentos da integração Elastic
Claroty xDome e calcula KPIs operacionais e executivos *depois* de
deduplicar alertas, normalizar IDs do ATT&CK for ICS v20.0 e separar
comportamento adversário de exposição/postura.

Princípios: biblioteca padrão apenas, offline, sem sockets, sem acesso a
SIEM, API de fornecedor ou ativo OT. O resultado é um envelope JSON com
digest SHA-256 (integridade, não autoria) e um relatório HTML estático.
"""

__version__ = "0.1.0"
