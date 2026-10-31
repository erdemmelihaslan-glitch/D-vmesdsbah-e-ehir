#!/usr/bin/env python3
"""Meta kampanyalarını ve reklam setlerini API ile kurar (resmi SDK: github.com/meta/facebook-python-business-sdk).

    python3 tools/meta_kur.py                 # KURU ÇALIŞMA: sadece ne kurulacağını gösterir
    python3 tools/meta_kur.py --uygula        # Gerçekten kurar — hepsi DURAKLATILMIŞ (PAUSED)

Gerekli ortam değişkenleri (asla dosyaya yazma, repoya koyma):
    META_ACCESS_TOKEN   Business Manager > Sistem kullanıcısı > Token (ads_management izni)
    META_AD_ACCOUNT_ID  Reklam hesabı numarası (act_ olmadan)
    META_PAGE_ID        Facebook sayfa ID'si (WhatsApp/Instagram bu sayfaya bağlı olmalı)

Neyi KURMAZ: reklam görselleri/videoları (kreatifler). Onları Ads Manager'da
reklam setinin içine ekle — ads/meta/kampanyalar.yaml'daki metinleri kopyala.
Her şey PAUSED kurulur; kontrol ettikten sonra Ads Manager'dan sen açarsın.

NOT: Bu script gerçek bir reklam hesabına karşı test edilmedi (hesap bağlantısı yoktu).
Meta API alan adları sürümle değişebilir; hata alırsan mesajı Claude'a göster.
"""
from __future__ import annotations

import argparse
import os
import sys

from ortak import ayarlar, yukle

GUN = 30.4


def hedefleme(cfg: dict, kamp: dict) -> dict:
    h = cfg["hedefleme"]
    k = cfg["studyo"]["konum"]
    t = {
        "geo_locations": {
            "custom_locations": [{
                "latitude": k["enlem"], "longitude": k["boylam"],
                "radius": h["yaricap_km"], "distance_unit": "kilometer",
            }],
        },
        "age_min": max(18, h["yas_min"]),   # 18 altı asla
        "publisher_platforms": ["instagram", "facebook"],
        "instagram_positions": ["stream", "story", "reels", "explore"],
        "facebook_positions": ["feed", "story", "facebook_reels"],
        # Advantage+ kitle: Meta yaşı/ilgiyi genişletebilir ama age_min sabit kalır
        "targeting_automation": {"advantage_audience": 1},
    }
    if kamp.get("ozel_kitle_idleri"):
        t["custom_audiences"] = [{"id": i} for i in kamp["ozel_kitle_idleri"]]
        t["targeting_automation"] = {"advantage_audience": 0}
        t["age_max"] = h["yas_max"]
    if kamp.get("haric_kitle_idleri"):
        t["excluded_custom_audiences"] = [{"id": i} for i in kamp["haric_kitle_idleri"]]
    return t


def plan(cfg: dict) -> list[dict]:
    meta = yukle("ads/meta/kampanyalar.yaml")
    aylik = cfg["butce"]["aylik_toplam_tl"]
    dag = cfg["butce"]["dagilim"]
    cikti = []
    for k in meta["kampanyalar"]:
        if k["kod"] == "K3" and not k.get("ozel_kitle_idleri"):
            print(f"⏭  {k['kod']} atlandı: önce özel kitleleri oluştur, ID'leri kampanyalar.yaml'a yaz.")
            continue
        setler = k["reklam_setleri"]
        gunluk = aylik * dag[k["butce_anahtari"]] / GUN / len(setler)
        for s in setler:
            adset = {
                "name": s["ad"],
                "daily_budget": int(round(gunluk)) * 100,   # kuruş cinsinden
                "billing_event": "IMPRESSIONS",
                "optimization_goal": k["optimizasyon"],
                "destination_type": k["hedef_yeri"],
                "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
                "targeting": hedefleme(cfg, k),
                "status": "PAUSED",
            }
            if k["optimizasyon"] == "CONVERSATIONS":
                adset["promoted_object"] = {"page_id": os.environ.get("META_PAGE_ID", "<META_PAGE_ID>")}
            cikti.append({"kampanya": {
                "name": k["ad"], "objective": k["amac"], "status": "PAUSED",
                "special_ad_categories": [],
                "is_adset_budget_sharing_enabled": False,
            }, "kod": k["kod"], "adset": adset, "gunluk_tl": round(gunluk)})
    return cikti


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--uygula", action="store_true", help="Gerçekten kur (PAUSED)")
    a = ap.parse_args()
    cfg = ayarlar()
    p = plan(cfg)

    print("\nKurulacaklar (hepsi DURAKLATILMIŞ):")
    for x in p:
        t = x["adset"]["targeting"]
        print(f"  {x['kod']:3} {x['kampanya']['name']}")
        print(f"      └ {x['adset']['name']}  · {x['gunluk_tl']} TL/gün · "
              f"{x['adset']['optimization_goal']} → {x['adset']['destination_type']} · "
              f"{t['geo_locations']['custom_locations'][0]['radius']} km · {t['age_min']}+")

    if not a.uygula:
        print("\nKuru çalışma. Kurmak için:  python3 tools/meta_kur.py --uygula")
        return

    eksik = [v for v in ("META_ACCESS_TOKEN", "META_AD_ACCOUNT_ID", "META_PAGE_ID") if not os.environ.get(v)]
    if eksik:
        sys.exit(f"Eksik ortam değişkeni: {', '.join(eksik)}")
    try:
        from facebook_business.adobjects.adaccount import AdAccount
        from facebook_business.api import FacebookAdsApi
    except ImportError:
        sys.exit("SDK yok:  pip install -r tools/requirements.txt")

    FacebookAdsApi.init(access_token=os.environ["META_ACCESS_TOKEN"])
    hesap = AdAccount(f"act_{os.environ['META_AD_ACCOUNT_ID']}")
    kurulan = {}
    for x in p:
        ad = x["kampanya"]["name"]
        if ad not in kurulan:
            kurulan[ad] = hesap.create_campaign(params=x["kampanya"])["id"]
            print(f"✔ Kampanya: {ad} ({kurulan[ad]})")
        params = dict(x["adset"], campaign_id=kurulan[ad])
        r = hesap.create_ad_set(params=params)
        print(f"   ✔ Reklam seti: {x['adset']['name']} ({r['id']})")
    print("\nŞimdi Ads Manager'da her reklam setine kreatifleri ekle, kontrol et ve yayına al.")


if __name__ == "__main__":
    main()
