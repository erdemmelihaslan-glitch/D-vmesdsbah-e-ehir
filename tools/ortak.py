"""Tüm araçların ortak kullandığı yardımcılar: ayar okuma, {alan} doldurma, stil filtresi."""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML gerekli:  pip install -r tools/requirements.txt")

KOK = Path(__file__).resolve().parent.parent
CIKTI = KOK / "cikti"


def yukle(goreli_yol: str) -> dict:
    with open(KOK / goreli_yol, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def ayarlar() -> dict:
    return yukle("config/studio.yaml")


def degiskenler(cfg: dict) -> dict:
    """Metinlerde {alan} olarak kullanılabilen değerler."""
    s = cfg.get("studyo", {})
    f = cfg.get("fiyatlar", {})
    d = {k: v for k, v in s.items() if not isinstance(v, dict)}
    d["studyo_adi"] = s.get("adi", "")
    d.update({k: _tl(v) for k, v in f.items()})
    return d


def _tl(sayi) -> str:
    """15000 -> '15.000' (Türkçe binlik ayırıcı)."""
    try:
        return f"{int(sayi):,}".replace(",", ".")
    except (TypeError, ValueError):
        return str(sayi)


tl = _tl

_ALAN = re.compile(r"\{([a-z_]+)\}")


def doldur(metin: str, d: dict) -> str:
    if not isinstance(metin, str):
        return metin
    return _ALAN.sub(lambda m: str(d.get(m.group(1), m.group(0))), metin)


def doldurulmamis(metin: str) -> list[str]:
    """Doldurulmamış {alan} ve 'DOLDUR' işaretlerini döndürür."""
    if not isinstance(metin, str):
        return []
    eksik = _ALAN.findall(metin)
    if "DOLDUR" in metin:
        eksik.append("DOLDUR")
    return eksik


def stil_acik(cfg: dict, oge: dict) -> bool:
    stil = oge.get("gerekli_stil")
    return not stil or bool(cfg.get("stiller", {}).get(stil, False))


def wa_link(telefon: str, mesaj: str) -> str:
    from urllib.parse import quote

    return f"https://wa.me/{telefon}?text={quote(mesaj)}"


def slug(metin: str) -> str:
    tablo = str.maketrans("çğıöşüÇĞİÖŞÜ ", "cgiosuCGIOSU-")
    return re.sub(r"[^a-zA-Z0-9-]", "", metin.translate(tablo)).lower()
