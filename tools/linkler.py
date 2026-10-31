#!/usr/bin/env python3
"""Her reklam için takip linkleri üretir → cikti/linkler.csv

    python3 tools/linkler.py

İki tür link:
  1) UTM'li web linki  — Google Analytics / Umami hangi reklamdan geldiğini görür
  2) WhatsApp linki    — hazır mesajın sonuna (R1) gibi KOD eklenir (hızlı soruların sonuna da).
     Müşteri yazdığında kodu görürsün → takip/musteri-takip.csv'ye "kaynak" olarak yaz.
     Böylece hangi reklamın RANDEVU getirdiğini bilirsin (sadece tıklama değil).
"""
from __future__ import annotations

import csv
from urllib.parse import urlencode

from ortak import CIKTI, ayarlar, degiskenler, doldur, slug, stil_acik, wa_link, yukle


def main():
    cfg = ayarlar()
    d = degiskenler(cfg)
    tel = cfg["studyo"]["telefon_whatsapp"]
    web = cfg["takip"].get("utm_kaynak_web") or cfg["studyo"]["web_sitesi"]
    satirlar = []

    meta = yukle("ads/meta/kampanyalar.yaml")
    for k in meta["kampanyalar"]:
        for s in k["reklam_setleri"]:
            for r in s["reklamlar"]:
                if not stil_acik(cfg, r):
                    continue
                utm = urlencode({"utm_source": "instagram", "utm_medium": "paid_social",
                                 "utm_campaign": slug(k["ad"].split("|")[1].strip()) + f"-{k['kod'].lower()}",
                                 "utm_content": r["kod"].lower()})
                mesaj = doldur(r.get("karsilama", "Merhaba! Bilgi almak istiyorum."), d)
                sorular = " | ".join(f"{s} ({r['kod']})" for s in meta.get("ortak", {}).get("hizli_sorular", []))
                satirlar.append({"kanal": "Meta", "kod": r["kod"], "kampanya": k["ad"], "faz": r.get("faz", ""),
                                 "hazir_mesaj": f"{mesaj} ({r['kod']})", "hizli_sorular": sorular,
                                 "web_linki": f"{web}?{utm}",
                                 "whatsapp_linki": wa_link(tel, f"{mesaj} ({r['kod']})")})

    g = yukle("ads/google/kampanya.yaml")
    for i, ag in enumerate(g["reklam_gruplari"], 1):
        if not stil_acik(cfg, ag):
            continue
        kod = f"G1-AG{i}"
        utm = urlencode({"utm_source": "google", "utm_medium": "cpc",
                         "utm_campaign": "g1-arama", "utm_content": slug(ag["ad"]),
                         "utm_term": "{keyword}"})
        satirlar.append({"kanal": "Google", "kod": kod, "kampanya": ag["ad"], "faz": 2,
                         "hazir_mesaj": "", "hizli_sorular": "",
                         "web_linki": f"{web}?{utm}".replace("%7Bkeyword%7D", "{keyword}"),
                         "whatsapp_linki": wa_link(tel, f"Merhaba! Google'dan ulaşıyorum, dövme için bilgi almak istiyorum. ({kod})")})

    # Organik / ücretsiz kaynaklar — bio linki, Google profil, QR kart
    for kod, ad, msg in [
        ("ORG-BIO", "Instagram bio linki", "Merhaba! Instagram'dan ulaşıyorum."),
        ("ORG-GMB", "Google İşletme Profili", "Merhaba! Google Haritalar'dan ulaşıyorum."),
        ("ORG-QR", "Stüdyo kartı / QR", "Merhaba! Kartınızdan ulaşıyorum."),
        ("ORG-REF", "Arkadaş tavsiyesi", "Merhaba! Bir arkadaşımın tavsiyesiyle yazıyorum."),
    ]:
        satirlar.append({"kanal": "Organik", "kod": kod, "kampanya": ad, "faz": "",
                         "hazir_mesaj": f"{msg} ({kod})", "hizli_sorular": "",
                         "web_linki": f"{web}?utm_source={slug(ad)}&utm_medium=organic",
                         "whatsapp_linki": wa_link(tel, f"{msg} ({kod})")})

    CIKTI.mkdir(exist_ok=True)
    yol = CIKTI / "linkler.csv"
    with open(yol, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(satirlar[0]))
        w.writeheader()
        w.writerows(satirlar)
    for s in satirlar:
        print(f"{s['kod']:10} {s['whatsapp_linki'][:90]}")
    print(f"\n✔ {len(satirlar)} link → {yol.relative_to(CIKTI.parent)}")


if __name__ == "__main__":
    main()
