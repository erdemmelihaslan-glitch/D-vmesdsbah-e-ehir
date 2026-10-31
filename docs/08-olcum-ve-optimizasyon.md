# 08 · Ölçüm ve Optimizasyon: Hangi Reklam Para Kazandırıyor?

## Neden çoğu stüdyo kör uçar?
Ads Manager sana "38 sohbet başladı" der. Ama bu 38 kişiden kaçının **kapora verdiğini** bilmez. Bu sistemin farkı şu: hazır mesajdaki **[KOD]** sayesinde her randevuyu bir reklama bağlıyoruz.

```
Reklam K2-02  →  Müşteri yazıyor: "...fiyat almak istiyorum. [K2-02]"
              →  takip/musteri-takip.csv: kaynak_kodu = K2-02, durum = kapora
              →  tools/rapor.py: "K2-02: 4 talep, 1 randevu, 2.500 TL"
```

## Haftalık rutin (her pazartesi, 20 dk)

1. **Ads Manager → Raporlar:** Son 7 gün, kampanya düzeyi. `takip/harcama.csv` dosyasına bir satır ekle:
   `hafta_baslangic, kod (K1/K2/K3/G1), harcama_tl, gosterim, tiklama, mesaj`
   Google Ads için de aynı şekilde G1 satırı.
2. **Müşteri takip** dosyasının güncel olduğundan emin ol (durumlar: `yeni`, `fiyat_verildi`, `kapora`, `tamamlandi`, `kayip`).
3. Raporu çalıştır:
   ```bash
   python3 tools/rapor.py            # son 7 gün
   python3 tools/rapor.py --gun 30   # aylık
   ```
4. Rapordaki **"Ne yapmalı?"** önerilerini uygula. Ya da Claude'a "haftalık raporu çıkar" de (skill: `haftalik-rapor`).

> Claude'a Meta veya Google hesabını bağlarsan 1. adımı Claude kendisi çeker (bkz. 09 → MCP).

## Karar kuralları

| Durum | Ne yap |
|---|---|
| Reklam ≥ 1.000 TL harcadı, mesaj başı maliyeti hedefin **2 katı** | Durdur, yeni kanca ile yeni reklam aç |
| Mesaj başı maliyet hedefin **%70'inin altında** | Bütçeyi **3 günde bir %20** artır |
| ROAS ≥ 5x ve ≥ 2 randevu | Bütçe artışında öncelik bu kampanyada |
| Çok mesaj, az randevu (< %10) | **Reklam değil süreç sorunu.** Cevap hızını ve scriptleri kontrol et (07) |
| Az mesaj, yüksek gösterim | Kreatif sorunu: kanca zayıf ya da metin net değil |
| Frekans > 3 | Kreatif yorgunluğu: yeni video |
| Google'da tıklama var, WhatsApp tıklaması yok | Landing sayfası sorunu: buton yukarıda mı, sayfa hızlı mı? |

## Ne zaman karar verilir?
- **72 saatten önce asla.** Meta öğrenme dönemindedir.
- Reklam başına en az **~1.000 TL** harcama ya da **7 gün** dolmadan "kötü" deme.
- Tek seferde **tek değişken** değiştir (ya kreatif ya bütçe ya kitle).

## Aylık kontrol
- Varsayımları güncelle: `config/studio.yaml` → `varsayimlar` (gerçek mesaj başı maliyeti ve dönüşüm oranları)
- `python3 tools/butce.py`: güncel verilerle gelecek ayın planı
- Hangi **stil** daha çok randevu getiriyor? Bütçeyi o stilin reklamlarına kaydır.
- Rakip kontrolü: Meta Reklam Kütüphanesi'nde Bahçeşehir rakipleri şu an ne yayınlıyor?

## Web analitiği (isteğe bağlı)
Landing sayfası kullanıyorsan **Umami** (ücretsiz, açık kaynak, çerezsiz) veya Google Analytics 4 ile UTM'leri takip et. `cikti/linkler.csv` dosyasındaki tüm linkler UTM'li.
