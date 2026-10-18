"""Digest SHA-256 para integridade de resultados offline, sem assinatura criptográfica."""
import hashlib
import json


def canonical_json(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def seal(payload):
    """Calcula hash sobre a representação JSON canônica do payload."""
    digest = hashlib.sha256(canonical_json(payload)).hexdigest()
    return {"algorithm": "sha256", "digest": digest, "payload": payload}


def verify(envelope):
    """Verifica alteração acidental/deliberada do payload contra o hash declarado.

    Um hash independente **não** garante autoria ou autenticidade. Para isso
    seriam necessários assinatura digital e armazenamento/ancoragem confiável.
    """
    if envelope.get("algorithm") != "sha256":
        return False
    digest = envelope.get("digest")
    if not isinstance(digest, str) or len(digest) != 64:
        return False
    try:
        return hashlib.sha256(canonical_json(envelope["payload"])).hexdigest() == digest
    except (KeyError, TypeError, ValueError):
        return False
