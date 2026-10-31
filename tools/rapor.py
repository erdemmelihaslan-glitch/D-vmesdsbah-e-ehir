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

from ortak import CIKTI, KOK, ayarlar, tl, yukle

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

    kpi = cfg.get("kpi", {})
    hedef_mesaj = kpi.get("hedef_mesaj_basi_tl", cfg["varsayimlar"]["mesaj_basi_maliyet_tl"][1])
    ort_is = cfg["fiyatlar"]["ortalama_is_tutari"]
    kapora_hedef = ort_is * kpi.get("kapora_basi_hedef_orani", 0.25)
    kapora_dur = ort_is * kpi.get("kapora_basi_durdur_orani", 0.5)

    # Kod → kampanya eşlemesi (reklam kodu "R1", set kodu "A1", kampanya "A" → "A")
    harita = {}
    for kk in yukle("ads/meta/kampanyalar.yaml").get("kampanyalar", []):
        harita[kk["kod"].upper()] = kk["kod"].upper()
        for s in kk.get("reklam_setleri", []):
            harita[s["kod"].upper()] = kk["kod"].upper()
            for r in s.get("reklamlar", []):
                harita[r["kod"].upper()] = kk["kod"].upper()

    def kampanya_of(kod: str) -> str:
        kod = kod.strip().upper()
        if kod.startswith("ORG"):
            return "ORGANIK"
        if kod in harita:
            return harita[kod]
        return kod.split("-")[0]

    kamp = defaultdict(lambda: defaultdict(float))
    for r in harcama:
        k = kampanya_of(r["kod"])
        for alan in ("harcama_tl", "gosterim", "tiklama", "mesaj"):
            kamp[k][alan] += sayi(r.get(alan))

    reklam = defaultdict(lambda: defaultdict(float))
    for m in musteriler:
        kod = (m.get("kaynak_kodu") or "BILINMIYOR").strip().upper()
        k = kampanya_of(kod)
        durum = (m.get("durum") or "").strip()
        odenen, teklif = sayi(m.get("odenen_tl")), sayi(m.get("teklif_tl"))
        for hedef in (kamp[k], reklam[kod]):
            hedef["talep"] += 1
            hedef["ciddi"] += durum in CIDDI
            hedef["randevu"] += durum in KAZANILAN
            hedef["tahsil"] += odenen                                   # kasaya giren
            hedef["rezerve"] += max(0.0, teklif - odenen) if durum in KAZANILAN else 0  # kaporalı, henüz ödenmemiş
            hedef["ciro"] += odenen + (max(0.0, teklif - odenen) if durum in KAZANILAN else 0)

    satir = []
    p = satir.append
    p(f"# Reklam Raporu — {bas:%d.%m.%Y} – {son:%d.%m.%Y}" + ("  (ÖRNEK VERİ)" if a.ornek else ""))
    p("")
    ucretli = {k: v for k, v in kamp.items() if k not in ("ORGANIK", "BILINMIYOR")}
    top_h = sum(v["harcama_tl"] for v in ucretli.values())
    top_r = sum(v["randevu"] for v in ucretli.values())
    top_c = sum(v["ciro"] for v in ucretli.values())
    top_t = sum(v["talep"] for v in ucretli.values())
    top_ts = sum(v["tahsil"] for v in ucretli.values())
    top_ciddi = sum(v["ciddi"] for v in ucretli.values())
    kb = top_h / top_r if top_r else 0
    p(f"**Reklam harcaması:** {tl(top_h)} TL · **Talep:** {top_t:.0f} (ciddi {top_ciddi:.0f}) · **Kapora/randevu:** {top_r:.0f}")
    p(f"**Kapora başı maliyet:** {tl(kb) + ' TL' if kb else '–'} (hedef ≤ {tl(kapora_hedef)} · durdur > {tl(kapora_dur)}) · "
      f"**Tahsil edilen:** {tl(top_ts)} TL · **Rezerve:** {tl(top_c - top_ts)} TL · **ROAS (toplam):** {(top_c / top_h if top_h else 0):.1f}x")
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
          f"{v['randevu']:.0f} | {tl(rb) if rb else '–'} | {tl(v['ciro'])} | {f'{roas:.1f}x' if h else '–'} |")
    p("")
    p("## Reklam bazında (müşteri takibinden)")
    p("| Kod | Talep | Ciddi | Randevu | Dönüşüm | Ciro |")
    p("|---|---:|---:|---:|---:|---:|")
    for kod, v in sorted(reklam.items(), key=lambda x: -x[1]["randevu"]):
        p(f"| {kod} | {v['talep']:.0f} | {v['ciddi']:.0f} | {v['randevu']:.0f} | "
          f"%{100 * v['randevu'] / v['talep']:.0f} | {tl(v['ciro'])} |")

    # ---- Karar kuralları (kurul tur 2: bütçe artışı SADECE Faz 2 kontrol listesi + sahip onayıyla) ----
    oneriler = []
    ilk = min([d for d in tarihler if d] or [son])
    gun = (son - ilk).days + 1
    for k, v in sorted(kamp.items()):
        h = v["harcama_tl"]
        if h == 0 or k in ("ORGANIK", "BILINMIYOR"):
            continue
        if h > kapora_dur and (not v["randevu"] or h / v["randevu"] > kapora_dur) and gun >= kpi.get("kapora_basi_durdur_en_erken_gun", 30):
            oneriler.append(f"🔴 **{k}**: {tl(h)} TL harcandı, kapora başı > {tl(kapora_dur)} TL (ya da hiç kapora yok). Kurul kuralı: DURDUR ve revize et.")
        elif h > kapora_dur and not v["randevu"]:
            oneriler.append(f"🟠 **{k}**: {tl(h)} TL harcandı ve henüz kapora yok. {kpi.get('kapora_basi_durdur_en_erken_gun', 30)}. günde hâlâ yoksa durdurulur.")
        if v["mesaj"]:
            mb = h / v["mesaj"]
            if mb > kpi.get("gun7_durdur_mesaj_basi_tl", 2 * hedef_mesaj) and gun >= 7:
                oneriler.append(f"🔴 **{k}**: sohbet başı {tl(mb)} TL (hedef {hedef_mesaj}). En kötü 2 reklamı kapat, yeni kanca dene (7. gün tek düzenleme).")
            ciddi_oran = v["ciddi"] / v["talep"] if v["talep"] else 0
            if 45 <= mb <= 50 and ciddi_oran >= 0.30 and 7 <= gun < 14:
                yeni = min(kpi.get("gun7_ogrenme_istisnasi", {}).get("tavan_tl", 360), round(7.2 * mb))
                oneriler.append(f"🟡 **{k}**: öğrenme istisnası koşulu sağlandı → günlük bütçe {yeni} TL (sahibin ön onayıyla).")
        if v["talep"] >= 8 and v["randevu"] / v["talep"] < 0.10:
            oneriler.append(f"🟠 **{k}**: {v['talep']:.0f} talepten {v['randevu']:.0f} randevu. Sorun büyük ihtimalle reklamda değil, "
                            "mesaj sürecinde → docs/07-mesaj-scriptleri.md (≤ 30 dk cevap + fiyat aralığıyla birlikte soru sor).")
        # Faz 2 kontrol listesi
        ciddi_oran = v["ciddi"] / v["talep"] if v["talep"] else 0
        mb = h / v["mesaj"] if v["mesaj"] else 0
        liste = [
            (f"en erken {kpi.get('faz2_en_erken_gun', 14)}. gün (şu an {gun})", gun >= kpi.get("faz2_en_erken_gun", 14)),
            (f"≥ 60 sohbet ({v['mesaj']:.0f})", v["mesaj"] >= 60),
            (f"sohbet başı ≤ 50 TL ({tl(mb) if mb else '–'})", 0 < mb <= 50),
            (f"ciddi talep ≥ %30 (%{100 * ciddi_oran:.0f})", ciddi_oran >= 0.30),
            (f"≥ 2 kapora ({v['randevu']:.0f})", v["randevu"] >= 2),
        ]
        tamam = all(ok for _, ok in liste)
        isaret = " · ".join(("✔ " if ok else "✘ ") + ad for ad, ok in liste)
        oneriler.append(f"{'🟢' if tamam else '⏳'} **{k} Faz 2 kontrolü:** {isaret} · ? 30 gün içinde ≥ 6 boş seans · ? cevap medyanı ≤ 30 dk"
                        + (" → iki elle kontrol de ✔ ise **sahibin onayıyla** 3 günde bir %20 artış (tavan 450 TL/gün)." if tamam else ""))
    tekrar = [m for m in musteriler if (m.get("tekrar") or "").strip().lower() == "e"]
    if musteriler and "tekrar" in musteriler[0]:
        oran = len(tekrar) / len(musteriler)
        esik = kpi.get("tekrar_yazan_esik", 0.15)
        if oran > esik:
            oneriler.append(f"🟠 Tekrar yazanların oranı %{100 * oran:.0f} > %{100 * esik:.0f}: hariç tutma kararı Politika üyesiyle yeniden değerlendirilmeli.")
    bekleyen = [m for m in musteriler if (m.get("durum") or "").strip() in ("yeni", "fiyat_verildi")]
    if bekleyen:
        oneriler.append(f"📲 **{len(bekleyen)} açık talep** (yeni / fiyat verildi). Bugün takip mesajı at: "
                        "docs/07-mesaj-scriptleri.md → 'Takip 1'.")
    yorumsuz = [m for m in musteriler if m.get("durum", "").strip() == "tamamlandi" and m.get("yorum_istendi", "").strip() != "e"]
    if yorumsuz:
        oneriler.append(f"⭐ {len(yorumsuz)} tamamlanmış işten Google yorumu istenmemiş. Yorum = bedava reklam.")
    if not oneriler:
        oneriler.append("Veri az. 72 saat dokunma; kararları set düzeyinde ver. 150 TL harcayıp 0 sohbet getiren reklamı kapat.")
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
