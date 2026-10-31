# 03 · Meta (Instagram + Facebook) Kurulum Rehberi

Kampanyaların tüm metinleri `ads/meta/kampanyalar.yaml` dosyasında. Bu rehber, onları **Ads Manager'a nasıl gireceğini** adım adım anlatıyor.

Üç kurulum yolu var:
- **A) Elle:** Bu rehberi takip et (önerilen ilk kurulum, ~45 dk)
- **B) Script:** `python3 tools/meta_kur.py --uygula` kampanya ve reklam setlerini PAUSED kurar, kreatifleri sen eklersin
- **C) Claude ile:** Meta reklam hesabını Claude'a bağla (bkz. `09-acik-kaynak-araclar.md` → MCP). Kurulum ve haftalık raporlama sohbetten yapılır.

---

## 0. Ön hazırlık (bir kez)

1. **business.facebook.com** → İşletme hesabı oluştur ya da mevcut hesabını aç.
2. **Hesaplar → Sayfalar:** Facebook sayfanı ekle.
3. **Hesaplar → Instagram hesapları:** Instagram'ı bağla (Profesyonel/İşletme hesabı olmalı).
4. **Hesaplar → WhatsApp hesapları:** WhatsApp **Business** numaranı bağla. Aynı numara sayfanın "WhatsApp butonu" olarak da görünsün.
5. **Ödeme yöntemi:** Kartı ekle. Para birimi **TRY**, saat dilimi **İstanbul**. ⚠️ Bunlar sonradan değiştirilemez.
6. **Events Manager → Pixel oluştur** (web siten ya da landing sayfan varsa). ID'yi `studio.yaml` → `takip.meta_pixel_id` alanına yaz.

## 1. Adlandırma kuralı (rapor için şart)
`K2 | Mesaj | WhatsApp | Sohbet` → reklam seti `K2-A | 18+ | Yarıçap | Advantage+ kitle` → reklam `K2-01`

Kod sistemi sayesinde `tools/rapor.py` hangi reklamın randevu getirdiğini eşleştirebilir.

## 2. K2: Mesaj kampanyası (önce bunu kur, ana kaynak bu)

**Kampanya düzeyi**
- Amaç: **Etkileşim** (Engagement)
- Kampanya bütçesi (Advantage+ bütçe): **KAPALI**. Bütçe reklam seti düzeyinde olacak.

**Reklam seti düzeyi**
- Dönüşüm konumu: **Mesajlaşma uygulamaları → WhatsApp** (istersen + Instagram)
- Performans hedefi: **Sohbetleri en üst düzeye çıkar**
- Bütçe: `python3 tools/butce.py` çıktısındaki "K2 günlük" tutarı (15.000 TL plan için ~246 TL/gün)
- Takvim: sürekli. Gece 01:00–08:00 arasını kapatmak istersen yalnızca ömür boyu bütçede mümkün, şimdilik sürekli bırak.
- **Kitle:**
  - Konum: stüdyonun adresine **sabitle** → yarıçap **12 km**
  - Konum tipi: "Bu konumda yaşayan veya yakın zamanda bulunan kişiler"
  - **Yaş alt sınırı: 18.** Advantage+ kitle açıkken bile "Kitle kontrolleri → Minimum yaş" 18 olmalı.
  - Advantage+ kitle: **AÇIK**. Öneri olarak 20–40 yaş ve "Dövme", "Body art", "Piercing" ilgilerini ekleyebilirsin.
  - Dil: Türkçe
- Yerleşimler: **Advantage+ yerleşimler** (otomatik). Audience Network kalabilir, mesajda sorun çıkarmaz.

**Reklam düzeyi** (K2-01 … K2-06)
- Kimlik: Facebook sayfası + Instagram hesabı
- Format: yaml'daki `format` alanı (carousel / reels / tekli görsel)
- Birincil metin, başlık: yaml'dan kopyala. `{alan}` yerlerini `studio.yaml` değerleriyle doldur.

  > İpucu: `python3 tools/linkler.py` çalıştır. `cikti/linkler.csv` dosyasında her reklamın doldurulmuş hazır mesajı var.
- **Mesaj şablonu → Hazır mesaj (karşılama):** yaml'daki `karsilama` metni + **sonuna kod**:
  `Merhaba! Minimal dövme için fiyat almak istiyorum. [K2-02]`
  Müşteri yazdığında kodu görürsün → takip dosyasına "kaynak_kodu" olarak yazarsın.
- CTA: **WhatsApp'tan mesaj gönder**

**Kaç reklam?** Bir reklam setine **3–5 reklam** koy. Mevsimlik olanları (`sezon:`) sadece zamanında aç.

## 3. K1: Keşif / Reels kampanyası

- Amaç: **Etkileşim** → Dönüşüm konumu: **Video** → Performans hedefi: **ThruPlay görüntülemelerini en üst düzeye çıkar**
- Kitle: K2 ile aynı (12 km, 18+, Advantage+)
- Yerleşim: Instagram ve Facebook **Reels + Hikâyeler** (dikey 9:16 video)
- Reklamlar: K1-01 … K1-04
- **Amaç satış değil.** Ucuza izlenme alırsın, izleyenler K3 için havuz olur. Başarı ölçütü: ThruPlay başı maliyet ve 3 saniye izlenme oranı.

## 4. K3: Yeniden hedefleme (2. haftadan sonra)

1. **Kitleler → Özel kitle oluştur:**
   - Instagram hesabı → "İşletmenizle etkileşim kuran herkes" → **60 gün**
   - Video → "Videonuzun en az %50'sini izleyen kişiler" (K1 videoları) → **30 gün**
   - Web sitesi (Pixel varsa) → Tüm ziyaretçiler → **30 gün**
   - Müşteri listesi (hariç tutmak için): KVKK onayı olan müşteri telefonları
2. Kitle ID'lerini `ads/meta/kampanyalar.yaml` → K3 → `ozel_kitle_idleri` alanına yaz.
3. K2 ile aynı ayarlar, ama **kitle = bu özel kitleler**, Advantage+ kitle **KAPALI**, bütçe ~49 TL/gün.

> Kitle 1.000 kişinin altındaysa K3 bekleyebilir. Önce K1 izlenme biriktirsin.

## 5. Yayından önce kontrol listesi
- [ ] `python3 tools/kontrol.py` → **hata yok**
- [ ] Tüm reklam setlerinde yaş alt sınırı **18**
- [ ] Hazır mesajların sonunda **[KOD]** var
- [ ] WhatsApp Business'ta **karşılama mesajı** ve **hızlı yanıtlar** hazır (bkz. 07)
- [ ] Reklamı açtığın gün **telefon elinde olsun**. İlk mesajlar 1 saat içinde gelir.

## 6. Öğrenme dönemi kuralları
- İlk **72 saat** hiçbir şeyi değiştirme.
- Bütçeyi bir seferde **%20'den fazla** artırma, yoksa öğrenme sıfırlanır.
- Reklam seti başına haftada ~**50 sohbet** hedeflenir. Küçük bütçede bu sayıya ulaşılamaz; bu yüzden reklam setlerini bölme, **tek geniş set** kullan.
- Reklam reddedilirse: Hesap Kalitesi → "İnceleme iste". Kapatma (öncesi/sonrası) reklamında sadece "sonra" görselini kullan.
