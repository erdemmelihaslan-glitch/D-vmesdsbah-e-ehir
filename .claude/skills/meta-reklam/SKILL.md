---
name: meta-reklam
description: Meta (Instagram + Facebook) reklamlarını kurma, güncelleme ve analiz etme — kampanya, reklam seti, bütçe, hedefleme, WhatsApp mesaj reklamları, Reels reklamları, yeniden hedefleme, özel kitle, Pixel, reklam reddi. Kullanıcı "Instagram reklamı", "Meta", "Facebook reklam", "Ads Manager", "kampanya kur", "bütçeyi artır", "reklam reddedildi", "mesaj başı maliyet" dediğinde kullan. Use for Meta/Instagram/Facebook ads setup, changes, targeting, budget and diagnostics for the tattoo studio.
---

# Meta Reklam Yönetimi

## Kaynak dosyalar
- `ads/meta/kampanyalar.yaml`: kampanya yapısı (K1 Keşif, K2 Mesaj, K3 Yeniden Hedefleme) ve tüm reklam metinleri
- `config/studio.yaml`: bütçe dağılımı, yarıçap, yaş, varsayımlar
- `docs/03-meta-kurulum.md`: Ads Manager adım adım kurulum
- `docs/08-olcum-ve-optimizasyon.md`: karar kuralları

## İş akışları

### A) Kampanya kurulumu
1. `python3 tools/kontrol.py` → hata varsa önce düzelt.
2. `python3 tools/butce.py` → günlük bütçeleri göster.
3. Yol seç:
   - **Meta MCP bağlıysa:** Kampanya → reklam seti → (kullanıcı görselleri verdiyse) reklam sırasıyla **PAUSED** kur. Her adımdan önce ne kurulacağını özetle ve **onay al**. Sonunda Ads Manager'da kontrol edip açmasını söyle.
   - **MCP yoksa:** `python3 tools/meta_kur.py` (kuru çalışma) çıktısını göster. Kullanıcı ortam değişkenlerini ayarladıysa `--uygula`. Ya da `docs/03-meta-kurulum.md` ile elle kurdur.
4. Her mesaj reklamının hazır mesajının sonuna **[REKLAM-KODU]** eklendiğini doğrula (ör. `[K2-02]`).

### B) Bütçe değişikliği
- Tek seferde en fazla **%20** artış, artışlar arasında **en az 3 gün**. Bütçeyi düşürmek serbest.
- Öğrenme dönemindeki (ilk 72 saat) bir sete dokunma.
- Değişikliği yapmadan önce: eski bütçe → yeni bütçe, gerekçe → **onay**.

### C) Performans teşhisi
Sırayla bak:
1. **Mesaj başı maliyet** (hedef `varsayimlar.mesaj_basi_maliyet_tl[1]`). 2 katını aşıyorsa sorun var.
2. **Kreatif:** 3 sn izlenme oranı / kaydırmayı durdurma oranı düşükse kanca zayıftır → `reklam-metni` skill'i ile yeni kanca yaz.
3. **Frekans > 3:** kreatif yorgunluğu.
4. **Mesaj çok, randevu az:** reklam değil, süreç sorunu → `musteri-mesaji` skill'i.
5. Karar kurallarının tamamı: `docs/08-olcum-ve-optimizasyon.md`.

### D) Reklam reddedildi
- Reddin nedenini oku. Sık nedenler: öncesi/sonrası görseli, çıplaklık ve ten fazlalığı, "kişisel özellik" ima eden dil ("Sen de dövme seven…").
- Düzelt: sadece "sonra" görseli, daha dar kadraj, genel dil. `tools/kontrol.py` ile denetle.
- Haklı olduğunu düşünüyorsan: Hesap Kalitesi → İnceleme iste.

### E) Yeniden hedefleme (K3)
- Özel kitleler: IG etkileşimi 60 gün, video %50 izleme 30 gün, site ziyaretçisi 30 gün. Hariç tut: müşteri listesi.
- Kitle < 1.000 kişiyse K3'ü açma, K1'in izlenme biriktirmesini bekle.
- Kitle ID'lerini `ads/meta/kampanyalar.yaml` → K3 → `ozel_kitle_idleri` alanına yaz.

## Sabit ayarlar (değiştirme)
- Yaş alt sınırı **18** (Advantage+ kitlede "minimum yaş" kontrolü)
- Konum: stüdyo çevresi **yarıçap** (`hedefleme.yaricap_km`), "yaşayan veya yakın zamanda bulunan"
- Küçük bütçede reklam setlerini bölme: **kampanya başına tek geniş set**
- Para birimi TRY, saat dilimi İstanbul

## Çıktı formatı
Kısa tablo (kampanya | harcama | mesaj | mesaj başı | randevu) + **en fazla 3 net aksiyon**, öncelik sırasıyla.
