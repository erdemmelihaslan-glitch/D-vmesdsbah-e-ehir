#!/usr/bin/env python3
"""Aylık bütçe planı ve beklenen sonuç senaryoları.

    python3 tools/butce.py                 # studio.yaml'daki bütçe
    python3 tools/butce.py --butce 7500    # farklı bütçe dene
    python3 tools/butce.py --karsilastir   # 7.500 / 15.000 / 30.000 TL yan yana

Not: Sonuçlar studio.yaml > varsayimlar alanındaki TAHMİNLERE dayanır.
İlk 14 günden sonra gerçek mesaj başı maliyetini oraya yaz, plan kendini düzeltir.
"""
from __future__ import annotations

import argparse

from ortak import ayarlar, tl

GUN = 30.4
ETIKET = {
    "meta_kesif_reels": "Meta Keşif (Reels)",
    "meta_mesaj": "A1 Meta Mesaj (WhatsApp)",
    "meta_yeniden_hedefleme": "B1 Meta Yeniden Hedefleme",
    "google_arama": "G1 Google Arama",
}
SENARYO = ["İyi", "Orta", "Kötü"]


def plan(cfg: dict, aylik: float) -> dict:
    b = cfg["butce"]
    v = cfg["varsayimlar"]
    f = cfg["fiyatlar"]
    if b.get("ucret_dahil"):
        aylik = aylik / (1 + b.get("ek_ucret_orani", 0))   # 10.000 TL ücret dahil → harcama ~9.524 TL
    kanallar = {k: aylik * oran for k, oran in b["dagilim"].items() if oran > 0}
    mesaj_butce = kanallar.get("meta_mesaj", 0) + kanallar.get("meta_yeniden_hedefleme", 0)
    google_butce = kanallar.get("google_arama", 0)

    senaryolar = []
    for i, ad in enumerate(SENARYO):
        meta_mesaj = mesaj_butce / v["mesaj_basi_maliyet_tl"][i]
        google_mesaj = google_butce / v["google_tik_maliyeti_tl"][i] * v["google_tik_mesaj_orani"]
        toplam_mesaj = meta_mesaj + google_mesaj
        ciddi = toplam_mesaj * v["gercek_musteri_orani"]
        oran = v["randevu_orani"]
        randevu = ciddi * (oran[i] if isinstance(oran, list) else oran)
        ciro = randevu * f["ortalama_is_tutari"]
        senaryolar.append(
            dict(ad=ad, mesaj=toplam_mesaj, ciddi=ciddi, randevu=randevu, ciro=ciro,
                 randevu_basi=aylik / randevu if randevu else 0,
                 roas=ciro / aylik if aylik else 0)
        )
    ana = kanallar.get("meta_mesaj", 0) / GUN
    ogrenme = [ana * 7 / m for m in v["mesaj_basi_maliyet_tl"]]   # haftalık sohbet (tek set)
    return dict(aylik=aylik, kanallar=kanallar, ek=aylik * b.get("ek_ucret_orani", 0),
                senaryolar=senaryolar, ogrenme=ogrenme, esik=50 * v["mesaj_basi_maliyet_tl"][1] / 7)


def yazdir(p: dict):
    print(f"\n══ AYLIK REKLAM PLANI: {tl(p['aylik'])} TL ══\n")
    print(f"{'Kanal':32}{'Aylık':>10}{'Günlük':>10}")
    for k, tutar in p["kanallar"].items():
        print(f"{ETIKET.get(k, k):32}{tl(tutar):>10}{tl(tutar / GUN):>10}")
    print(f"{'+ Meta konum ücreti vb. (tahmini)':32}{tl(p['ek']):>10}")
    print(f"{'TOPLAM ÇIKIŞ':32}{tl(p['aylik'] + p['ek']):>10}\n")

    print("Beklenen aylık sonuç (varsayımlara göre — garanti değildir; ortalama proje tutarı TAHMİN):")
    print(f"{'Senaryo':10}{'Mesaj':>8}{'Ciddi':>8}{'Randevu':>9}{'Randevu başı':>14}{'Ciro':>12}{'ROAS':>7}")
    for s in p["senaryolar"]:
        print(f"{s['ad']:10}{s['mesaj']:>8.0f}{s['ciddi']:>8.0f}{s['randevu']:>9.0f}"
              f"{tl(s['randevu_basi']):>11} TL{tl(s['ciro']):>9} TL{s['roas']:>6.1f}x")
    og = p["ogrenme"]
    print(f"\nÖğrenme (Meta: set başına ~50 sohbet/hafta): ana set haftada {og[0]:.0f} / {og[1]:.0f} / {og[2]:.0f} sohbet "
          f"(iyi/orta/kötü). Orta senaryoda 50 için gereken: ~{tl(p['esik'])} TL/gün.")
    print("ROAS = reklamdan gelen ciro / reklam harcaması. Ana ölçüt: kapora başı maliyet (config > kpi).")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--butce", type=float)
    ap.add_argument("--karsilastir", action="store_true")
    a = ap.parse_args()
    cfg = ayarlar()
    if a.karsilastir:
        for b in (7500, 15000, 30000):
            yazdir(plan(cfg, b))
    else:
        yazdir(plan(cfg, a.butce or cfg["butce"]["aylik_toplam_tl"]))


if __name__ == "__main__":
    main()
