---
name: haftalik-rapor
description: Dövme stüdyosunun haftalık/aylık reklam performans raporu — Meta ve Google harcaması, mesaj, randevu, ciro, ROAS, reklam bazında karşılaştırma ve "ne yapmalı" önerileri. Kullanıcı "reklamlar nasıl gidiyor", "haftalık rapor", "bu ay ne kadar harcadık", "hangi reklam iyi", "ROAS", "rapor çıkar" dediğinde kullan. Use for weekly or monthly ad performance reports with clear next actions.
---

# Haftalık Performans Raporu

## Veri toplama (sırayla dene)
1. **Canlı hesap:** Meta ya da Google MCP araçları bağlıysa son 7 günün kampanya düzeyi verisini çek: harcama, gösterim, tıklama, başlatılan mesajlaşma sohbeti (Meta), dönüşüm (Google). Çekilen veriyi `takip/harcama.csv` dosyasına **yeni satırlar olarak** ekle (kod: K1/K2/K3/G1).
2. **MCP yoksa:** Kullanıcıdan Ads Manager ve Google Ads ekran görüntüsü veya CSV iste, rakamları `takip/harcama.csv` dosyasına sen yaz.
3. **Müşteri takibi:** `takip/musteri-takip.csv` güncel mi? Değilse kullanıcıya sor: "Bu hafta kaç kişi yazdı, kaçı kapora verdi, hangi kodlarla geldiler?" Cevaplarla satırları ekle. Sadece baş harf, telefon numarası yazma.

## Raporu üret
```bash
python3 tools/rapor.py            # son 7 gün
python3 tools/rapor.py --gun 30   # aylık
```
Rapor `cikti/rapor-YYYY-AA-GG.md` dosyasına kaydedilir.

## Yorumla (kullanıcıya sunarken)
1. **Tek cümlelik özet:** "Bu hafta 3.500 TL harcadık, 5 randevu geldi, randevu başı 700 TL, ROAS 7,9x: iyi gidiyor."
2. **Kazanan:** En çok randevu getiren reklam kodu ve nedeni (hangi kanca/format)
3. **Kaybeden:** Durdurulacak reklam ve yerine ne konulacağı
4. **Süreç:** Açık talepler, cevaplanmamış mesajlar, istenmemiş Google yorumları
5. **En fazla 3 aksiyon**, öncelik sırasıyla. Para harcayan aksiyonlar için onay iste.

## Karar kuralları
`docs/08-olcum-ve-optimizasyon.md` tablosunu uygula. Özetle:
- 72 saatten ya da ~1.000 TL harcamadan önce "kötü" deme
- Mesaj başı maliyet hedefin 2 katıysa → durdur + yeni kanca
- Hedefin %70'inin altındaysa → 3 günde bir %20 bütçe artışı
- Çok mesaj, az randevu → sorun mesaj sürecinde (`musteri-mesaji` skill'i)

## Aylık ek adımlar
- Gerçek ortalamaları `config/studio.yaml` → `varsayimlar` alanına yaz (mesaj başı maliyet, oranlar)
- `python3 tools/butce.py` ile gelecek ayın planını güncel verilerle göster
- Mevsimsel takvime bak (`docs/06-icerik-takvimi.md`): gelecek ay hangi reklamlar açılmalı?
