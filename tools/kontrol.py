#!/usr/bin/env python3
"""Reklam setinin sağlık kontrolü.

    python3 tools/kontrol.py

Denetler:
  - studio.yaml'da doldurulmamış alanlar
  - Bütçe dağılımı toplamı = 1.00
  - Yaş alt sınırı ≥ 18
  - Google başlık ≤ 30, açıklama ≤ 90 karakter (doldurulmuş haliyle)
  - Meta başlık ≤ 40 karakter (tavsiye), birincil metin ilk satırı ≤ 125 karakter
  - Riskli / yasaklı ifadeler (Ticari Reklam Yönetmeliği + Meta politikaları)
Çıkış kodu: hata varsa 1.
"""
from __future__ import annotations

import re
import sys

from ortak import ayarlar, degiskenler, doldur, doldurulmamis, stil_acik, yukle

# Kanıtlanamayan üstünlük iddiaları, sağlık iddiaları, görünüşü aşağılayan ifadeler
RISKLI = {
    "en iyi": "Kanıtlanamayan üstünlük iddiası (Reklam Kurulu cezası riski)",
    "bir numara": "Kanıtlanamayan üstünlük iddiası",
    "1 numara": "Kanıtlanamayan üstünlük iddiası",
    "lider": "Kanıtlanamayan üstünlük iddiası",
    "garanti": "'Garanti' iddiası — yerine somut vaat yaz (ör. 'ücretsiz rötuş')",
    "%100": "Mutlak iddia",
    "acısız": "Yanıltıcı sağlık iddiası",
    "hiç acımaz": "Yanıltıcı sağlık iddiası",
    "çirkin": "Görünüş hakkında olumsuz ifade (Meta politikası)",
    "utanıyor": "Görünüş hakkında olumsuz ifade (Meta politikası)",
    "rezil": "Görünüş hakkında olumsuz ifade (Meta politikası)",
    "bedava": "Ücretsiz dövme izlenimi — düşük kaliteli talep çeker",
    "indirim son gün": "Sahte aciliyet riski — sadece gerçekse kullan",
    "steril ortam": "Kurul kararı: 'steril ortam' yerine 'sterilize ekipman' (kanıtlanabilir ifade)",
}
ROTUS_KOSULSUZ = False  # main(): rotus_suresi_ay belli değilse 'rötuş' ifadesi hata

hatalar: list[str] = []
uyarilar: list[str] = []


def hata(m):
    hatalar.append(m)


def uyari(m):
    uyarilar.append(m)


def tr_kucuk(metin: str) -> str:
    return metin.replace("İ", "i").replace("I", "ı").lower()


FIYAT_YASAK = False  # main() studio.yaml > reklam.fiyat_goster'a göre ayarlar
_FIYAT = re.compile(r"\d[\d.]*\s*(tl|₺)|₺\s*\d|_baslangic|kapora\}", re.I)


def riskli_tara(yer: str, metin: str):
    if ROTUS_KOSULSUZ and "rötuş" in tr_kucuk(metin or ""):
        hata(f"{yer}: 'rötuş' geçiyor ama studio.yaml > reklam.rotus_suresi_ay boş (şartsız 'ücretsiz' iddiası)")
    if FIYAT_YASAK and _FIYAT.search(metin or ""):
        hata(f"{yer}: fiyat geçiyor ama studio.yaml > reklam.fiyat_goster=false → '{metin.strip()[:60]}'")
    kucuk = tr_kucuk(metin)
    for ifade, neden in RISKLI.items():
        # kelime başında eşleşsin: "dövmen iyileşir" ≠ "en iyi"
        if re.search(rf"(?<!\w){re.escape(ifade)}", kucuk):
            hata(f"{yer}: '{ifade}' → {neden}")


def config_kontrol(cfg):
    def gez(d, yol=""):
        for k, v in d.items():
            p = f"{yol}.{k}" if yol else k
            if isinstance(v, dict):
                gez(v, p)
            elif isinstance(v, str) and "DOLDUR" in v:
                uyari(f"studio.yaml → {p} henüz doldurulmadı")

    gez(cfg)
    dag = cfg.get("butce", {}).get("dagilim", {})
    toplam = round(sum(dag.values()), 4)
    if abs(toplam - 1) > 0.001:
        hata(f"Bütçe dağılımı toplamı {toplam} — 1.00 olmalı")
    yas = cfg.get("hedefleme", {}).get("yas_min", 0)
    if yas < 18:
        hata(f"yas_min={yas}. 18 altı hedefleme YASAK (Meta + yasa teklifi).")


def meta_kontrol(cfg, d):
    meta = yukle("ads/meta/kampanyalar.yaml")
    sayac = 0
    for k in meta.get("kampanyalar", []):
        if k["butce_anahtari"] not in cfg["butce"]["dagilim"]:
            hata(f"{k['kod']}: butce_anahtari '{k['butce_anahtari']}' studio.yaml'da yok")
        for s in k.get("reklam_setleri", []):
            for r in s.get("reklamlar", []):
                if not stil_acik(cfg, r):
                    continue
                sayac += 1
                yer = f"Meta {r['kod']}"
                for alan in ("metin", "baslik", "ekran_yazisi", "karsilama"):
                    if alan not in r:
                        continue
                    m = doldur(r[alan], d)
                    for e in doldurulmamis(m):
                        uyari(f"{yer}.{alan}: '{e}' doldurulmadı")
                    riskli_tara(f"{yer}.{alan}", m)
                b = doldur(r.get("baslik", ""), d)
                if len(b) > 40:
                    uyari(f"{yer}: başlık {len(b)} karakter (>40, mobilde kesilebilir): {b}")
                ilk = doldur(r.get("metin", ""), d).strip().split("\n")[0]
                if len(ilk) > 125:
                    uyari(f"{yer}: metnin ilk satırı {len(ilk)} karakter (>125 'devamı' altında kalır)")
                if k["optimizasyon"] == "CONVERSATIONS" and not r.get("karsilama"):
                    hata(f"{yer}: mesaj reklamında 'karsilama' (hazır mesaj) yok")
    return sayac


def google_kontrol(cfg, d):
    g = yukle("ads/google/kampanya.yaml")
    sayac = 0
    for ag in g.get("reklam_gruplari", []):
        if not stil_acik(cfg, ag):
            continue
        sayac += 1
        yer = f"Google {ag['ad']}"
        bas = [doldur(x, d) for x in ag.get("basliklar", [])]
        acik = [doldur(x, d) for x in ag.get("aciklamalar", [])]
        if not 3 <= len(bas) <= 15:
            hata(f"{yer}: {len(bas)} başlık (3–15 olmalı)")
        if not 2 <= len(acik) <= 4:
            hata(f"{yer}: {len(acik)} açıklama (2–4 olmalı)")
        if len(set(bas)) != len(bas):
            hata(f"{yer}: tekrarlanan başlık var")
        for x in ag.get("basliklar", []) + ag.get("aciklamalar", []):
            if FIYAT_YASAK and _FIYAT.search(x):
                hata(f"{yer}: fiyat geçiyor ama reklam.fiyat_goster=false → '{x}'")
        for x in bas:
            if len(x) > 30:
                hata(f"{yer}: başlık {len(x)}>30 → '{x}'")
            riskli_tara(yer, x)
        for x in acik:
            if len(x) > 90:
                hata(f"{yer}: açıklama {len(x)}>90 → '{x}'")
            riskli_tara(yer, x)
        for y in ag.get("yol", []):
            if len(y) > 15:
                hata(f"{yer}: yol '{y}' >15 karakter")
    return sayac


def main():
    global FIYAT_YASAK, ROTUS_KOSULSUZ
    cfg = ayarlar()
    FIYAT_YASAK = not cfg.get("reklam", {}).get("fiyat_goster", True)
    ROTUS_KOSULSUZ = cfg.get("reklam", {}).get("rotus_suresi_ay") in (None, "", 0)
    d = degiskenler(cfg)
    config_kontrol(cfg)
    n_meta = meta_kontrol(cfg, d)
    n_google = google_kontrol(cfg, d)

    print(f"✔ {n_meta} Meta reklamı, {n_google} Google reklam grubu kontrol edildi.\n")
    if uyarilar:
        print(f"⚠ {len(uyarilar)} UYARI")
        for u in uyarilar:
            print("   -", u)
        print()
    if hatalar:
        print(f"✘ {len(hatalar)} HATA")
        for h in hatalar:
            print("   -", h)
        sys.exit(1)
    print("✔ Hata yok." + (" Uyarıları yayına almadan önce gider." if uyarilar else ""))


if __name__ == "__main__":
    main()
