#!/usr/bin/env python3
"""ads/google/kampanya.yaml → Google Ads Editor'e yüklenebilir CSV'ler.

    python3 tools/google_disa_aktar.py

Çıktı (cikti/google/):
  anahtar-kelimeler.csv   Campaign, Ad group, Keyword, Criterion Type
  reklamlar.csv           Duyarlı arama reklamları (RSA): 15 başlık / 4 açıklama
  negatifler.csv          Kampanya düzeyi negatif kelimeler

Google Ads Editor: Hesap > İçe aktar > Dosyadan → her CSV'yi sırayla seç → "Değişiklikleri incele" → Yayınla.
"""
from __future__ import annotations

import csv

from ortak import CIKTI, KOK, ayarlar, degiskenler, doldur, stil_acik, yukle


def eslesme(k: str) -> tuple[str, str]:
    k = k.strip()
    if k.startswith("[") and k.endswith("]"):
        return k[1:-1], "Exact"
    if k.startswith('"') and k.endswith('"'):
        return k[1:-1], "Phrase"
    return k, "Broad"


def yaz(yol, satirlar):
    with open(yol, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(satirlar[0]))
        w.writeheader()
        w.writerows(satirlar)
    print(f"✔ {len(satirlar):3} satır → {yol.relative_to(KOK)}")


def main():
    cfg = ayarlar()
    d = degiskenler(cfg)
    g = yukle("ads/google/kampanya.yaml")
    kampanya = g["kampanya"]["ad"]
    hedef = CIKTI / "google"
    hedef.mkdir(parents=True, exist_ok=True)

    kelimeler, reklamlar = [], []
    for ag in g["reklam_gruplari"]:
        if not stil_acik(cfg, ag):
            print(f"  (atlandı: {ag['ad']} — stil kapalı)")
            continue
        for k in ag["anahtar_kelimeler"]:
            kelime, tur = eslesme(k)
            kelimeler.append({"Campaign": kampanya, "Ad group": ag["ad"],
                              "Keyword": kelime, "Criterion Type": tur})
        r = {"Campaign": kampanya, "Ad group": ag["ad"], "Ad type": "Responsive search ad"}
        for i in range(15):
            r[f"Headline {i + 1}"] = doldur(ag["basliklar"][i], d) if i < len(ag["basliklar"]) else ""
        for i in range(4):
            r[f"Description {i + 1}"] = doldur(ag["aciklamalar"][i], d) if i < len(ag["aciklamalar"]) else ""
        yol = ag.get("yol", ["", ""]) + ["", ""]
        r.update({"Path 1": yol[0], "Path 2": yol[1], "Final URL": doldur(ag["final_url"], d)})
        reklamlar.append(r)

    negatifler = []
    for satir in (KOK / "ads/google/negatif-kelimeler.txt").read_text(encoding="utf-8").splitlines():
        satir = satir.strip()
        if satir and not satir.startswith("#"):
            negatifler.append({"Campaign": kampanya, "Keyword": satir, "Criterion Type": "Negative Broad"})

    yaz(hedef / "anahtar-kelimeler.csv", kelimeler)
    yaz(hedef / "reklamlar.csv", reklamlar)
    yaz(hedef / "negatifler.csv", negatifler)
    print("\nÖnce:  python3 tools/kontrol.py   (başlık/açıklama uzunlukları)")


if __name__ == "__main__":
    main()
