#!/usr/bin/env python3
"""Haftalık performans raporu + ne yapmalı önerileri.

    python3 tools/rapor.py               # takip/ klasöründeki gerçek veriler
    python3 tools/rapor.py --ornek       # örnek verilerle dene
    python3 tools/rapor.py --gun 30      # son 30 gün

Girdi:
  takip/harcama.csv       Haftalık harcama (Ads Manager / Google Ads'ten kopyala)
  takip/musteri-takip.csv Her WhatsApp/DM talebi bir satır (kaynak_kodu = mesajdaki [KOD])
Çıktı: ekrana + cikti/rapor-YYYY-AA-GG.md
"""
from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from datetime import date, datetime, timedelta

from ortak import CIKTI, KOK, ayarlar, tl

KAZANILAN = {"kapora", "tamamlandi"}
CIDDI = {"fiyat_verildi", "kapora", "tamamlandi"}


def oku(yol):
    if not yol.exists():
        return []
    with open(yol, encoding="utf-8-sig") as f:
        return [r for r in csv.DictReader(f) if any(v.strip() for v in r.values() if v)]


def sayi(x) -> float:
    try:
        return float(str(x).replace(".", "").replace(",", ".")) if x not in (None, "") else 0.0
    except ValueError:
        return 0.0


def tarih(x):
    try:
        return datetime.strptime(x.strip(), "%Y-%m-%d").date()
    except (ValueError, AttributeError):
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ornek", action="store_true")
    ap.add_argument("--gun", type=int, default=7)
    a = ap.parse_args()

    cfg = ayarlar()
    klasor = KOK / "takip" / ("ornek" if a.ornek else "")
    harcama = oku(klasor / "harcama.csv")
    musteriler = oku(klasor / "musteri-takip.csv")
    if not harcama and not musteriler:
        print("takip/ klasörü boş. Önce örnekle dene:  python3 tools/rapor.py --ornek")
        return

    # Dönem: en son kayıttan geriye --gun kadar
    tarihler = [tarih(r["tarih"]) for r in musteriler] + [tarih(r["hafta_baslangic"]) for r in harcama]
    son = max([t for t in tarihler if t] or [date.today()])
    bas = son - timedelta(days=a.gun - 1)
    harcama = [r for r in harcama if (t := tarih(r["hafta_baslangic"])) and t >= bas - timedelta(days=6)]
    musteriler = [r for r in musteriler if (t := tarih(r["tarih"])) and t >= bas]

    hedef_mesaj = cfg["varsayimlar"]["mesaj_basi_maliyet_tl"][1]
    ort_is = cfg["fiyatlar"]["ortalama_is_tutari"]

    kamp = defaultdict(lambda: defaultdict(float))
    for r in harcama:
        k = r["kod"].strip().upper()
        for alan in ("harcama_tl", "gosterim", "tiklama", "mesaj"):
            kamp[k][alan] += sayi(r.get(alan))

    reklam = defaultdict(lambda: defaultdict(float))
    for m in musteriler:
        kod = (m.get("kaynak_kodu") or "BILINMIYOR").strip().upper()
        k = kod.split("-")[0] if not kod.startswith("ORG") else "ORGANIK"
        durum = (m.get("durum") or "").strip()
        for hedef in (kamp[k], reklam[kod]):
            hedef["talep"] += 1
            hedef["ciddi"] += durum in CIDDI
            hedef["randevu"] += durum in KAZANILAN
            # Ciro: ödenen yoksa kaporalı işlerin teklifini beklenen ciro say
            hedef["ciro"] += sayi(m.get("odenen_tl")) or (sayi(m.get("teklif_tl")) if durum == "kapora" else 0)

    satir = []
    p = satir.append
    p(f"# Reklam Raporu — {bas:%d.%m.%Y} – {son:%d.%m.%Y}" + ("  (ÖRNEK VERİ)" if a.ornek else ""))
    p("")
    ucretli = {k: v for k, v in kamp.items() if k not in ("ORGANIK", "BILINMIYOR")}
    top_h = sum(v["harcama_tl"] for v in ucretli.values())
    top_r = sum(v["randevu"] for v in ucretli.values())
    top_c = sum(v["ciro"] for v in ucretli.values())
    top_t = sum(v["talep"] for v in ucretli.values())
    p(f"**Reklam harcaması:** {tl(top_h)} TL · **Reklamdan talep:** {top_t:.0f} · **Randevu:** {top_r:.0f} · "
      f"**Ciro:** {tl(top_c)} TL · **ROAS:** {(top_c / top_h if top_h else 0):.1f}x")
    org = kamp.get("ORGANIK")
    if org:
        p(f"_Organik (bio, Google profil, tavsiye): {org['talep']:.0f} talep, {org['randevu']:.0f} randevu, {tl(org['ciro'])} TL — ROAS'a dahil değil._")
    p("")
    p("| Kampanya | Harcama | Platform mesajı | Mesaj başı | Talep (takip) | Ciddi | Randevu | Randevu başı | Ciro | ROAS |")
    p("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for k in sorted(kamp):
        v = kamp[k]
        h = v["harcama_tl"]
        mb = h / v["mesaj"] if v["mesaj"] else 0
        rb = h / v["randevu"] if v["randevu"] else 0
        roas = v["ciro"] / h if h else 0
        p(f"| {k} | {tl(h)} | {v['mesaj']:.0f} | {tl(mb) if mb else '–'} | {v['talep']:.0f} | {v['ciddi']:.0f} | "
          f"{v['randevu']:.0f} | {tl(rb) if rb else '–'} | {tl(v['ciro'])} | {f'{roas:.1f}x' if h and k != 'K1' else '–'} |")
    p("")
    p("_K1 keşif kampanyasıdır: satış değil, izlenme ve yeniden hedefleme kitlesi üretir._")
    p("")
    p("## Reklam bazında (müşteri takibinden)")
    p("| Kod | Talep | Ciddi | Randevu | Dönüşüm | Ciro |")
    p("|---|---:|---:|---:|---:|---:|")
    for kod, v in sorted(reklam.items(), key=lambda x: -x[1]["randevu"]):
        p(f"| {kod} | {v['talep']:.0f} | {v['ciddi']:.0f} | {v['randevu']:.0f} | "
          f"%{100 * v['randevu'] / v['talep']:.0f} | {tl(v['ciro'])} |")

    # ---- Karar kuralları ----
    oneriler = []
    for k, v in sorted(kamp.items()):
        h = v["harcama_tl"]
        if k == "K1" or h == 0:
            continue
        if v["mesaj"]:
            mb = h / v["mesaj"]
            if mb > 2 * hedef_mesaj and h >= 1000:
                oneriler.append(f"🔴 **{k}**: mesaj başı {tl(mb)} TL (hedef ~{hedef_mesaj}). En kötü reklamı durdur, yeni kanca (ilk 2 sn) dene.")
            elif mb < 0.7 * hedef_mesaj:
                oneriler.append(f"🟢 **{k}**: mesaj başı {tl(mb)} TL — hedefin altında. Bütçeyi 3 günde bir %20 artır.")
        roas = v["ciro"] / h if h else 0
        if v["randevu"] >= 2 and roas >= 5:
            oneriler.append(f"🟢 **{k}**: ROAS {roas:.1f}x. Bu kampanya para basıyor — bütçe artışında öncelik bunda.")
        if v["talep"] >= 8 and v["randevu"] / v["talep"] < 0.10:
            oneriler.append(f"🟠 **{k}**: {v['talep']:.0f} talepten {v['randevu']:.0f} randevu. Sorun büyük ihtimalle reklamda değil, "
                            "mesaj sürecinde → docs/07-mesaj-scriptleri.md (5 dk içinde cevap + fiyatla birlikte soru sor).")
    bekleyen = [m for m in musteriler if (m.get("durum") or "").strip() in ("yeni", "fiyat_verildi")]
    if bekleyen:
        oneriler.append(f"📲 **{len(bekleyen)} açık talep** (yeni / fiyat verildi). Bugün takip mesajı at: "
                        "docs/07-mesaj-scriptleri.md → 'Takip 1'.")
    yorumsuz = [m for m in musteriler if m.get("durum", "").strip() == "tamamlandi" and m.get("yorum_istendi", "").strip() != "e"]
    if yorumsuz:
        oneriler.append(f"⭐ {len(yorumsuz)} tamamlanmış işten Google yorumu istenmemiş. Yorum = bedava reklam.")
    if not oneriler:
        oneriler.append("Veri az. En az 7 gün ve kampanya başına ~1.000 TL harcamadan karar verme.")
    p("")
    p("## Ne yapmalı?")
    for o in oneriler:
        p(f"- {o}")

    metin = "\n".join(satir)
    print(metin)
    CIKTI.mkdir(exist_ok=True)
    yol = CIKTI / f"rapor-{son:%Y-%m-%d}{'-ornek' if a.ornek else ''}.md"
    yol.write_text(metin + "\n", encoding="utf-8")
    print(f"\n✔ Kaydedildi → {yol.relative_to(KOK)}")


if __name__ == "__main__":
    main()
