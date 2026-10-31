# 10 · Mevzuat ve Platform Kuralları

> ⚠️ Bu bir hukuki görüş değildir. Kaynaklarla desteklenmiş bir **risk listesidir**. Vergi ve izin konularında muhasebecine, şüpheli durumlarda bir avukata danış.

## 1. Yaş: 18 altına dövme YOK
- **Mart 2026:** TBMM'ye sunulan kanun teklifi, 18 yaş altına dövme veya piercing yapanların **"kasten yaralama"** kapsamında yargılanmasını öngörüyor. Teklif gerekçesine göre mevcut mevzuatta bu konuda özel bir yaptırım yok. Kabul edilip edilmediği doğrulanamadı.
- Sağlık Bakanlığı'nın daha eski bir yönerge çalışmasında da 18 yaş altına dövme, 16 yaş altına piercing yasağı öngörülüyordu.
- **Uygulama:**
  - Her müşteriden **kimlik** iste, randevu mesajında hatırlat (07 → /kapora)
  - Tüm reklamlarda **yaş alt sınırı 18** (`tools/kontrol.py` bunu denetler)
  - İçeriklerde okul forması veya çocuk gibi görünen modeller kullanma

## 2. Meta reklam politikaları
- **Kozmetik işlemler:** sadece **18+** kişilere hedeflenebilir. Dövme politikada açıkça geçmiyor, ama 18+ en güvenli yol.
- **Yasak:** Görünüş hakkında **olumsuz ifade** ("Kolundaki o çirkin dövmeden utanıyor musun?"). Yerine olumlu çerçeve kullan: "Eski dövmen yeni bir hikâyeye dönüşebilir."
- **Öncesi/sonrası görseller:** Politika genel kozmetikte izin veriyor, ama otomatik inceleme dövme ve kapatma görsellerini işaretleyebiliyor. Reddedilirse sadece "sonra" görselini kullan ya da itiraz et.
- **Çıplaklık / ima:** Kalça, göğüs, kasık bölgesi dövmelerinde çıplaklık politikasına takılmamak için kadrajı dar tut, cinsel ima içeren poz kullanma.
- Kişisel özellik ima etme: "Sen de dövme seven biri misin?" gibi kişiye doğrudan özellik atfeden dil yerine genel dil kullan.

## 3. Türk reklam hukuku (Ticari Reklam ve Haksız Ticari Uygulamalar Yönetmeliği)
- **Kanıtlanamayan üstünlük iddiaları:** "En iyi", "bir numara", "lider", "en hijyenik" gibi ifadeler. Reklam Kurulu idari para cezası riski taşır. → `kontrol.py` bunları yakalar.
- **İndirim reklamları:** "İndirim öncesi fiyat" olarak gerçekten uygulanmış fiyat gösterilmeli (son 30 gün kuralı). Sahte "son gün" aciliyeti yaratma. → Bu yüzden indirim yerine **hediye kartı bonusu** öneriyoruz.
- **Sağlık iddiaları:** "Acısız", "%100 güvenli", "alerji yapmaz" gibi ifadeler kullanma.
- **Fiyat:** "X TL'den başlayan" ifadesi kullanılıyorsa, o fiyata gerçekten iş yapılıyor olmalı.

## 4. Müşteri verisi (KVKK)
- WhatsApp numarası, fotoğraf ve sağlık bilgisi (alerji vb.) kişisel veridir.
- **Aydınlatma metni:** Landing sayfasında ve seans öncesi onam formunda kısa bir metin bulunsun (`landing/index.html` içinde örnek var).
- **Fotoğraf paylaşımı:** Müşterinin **açık onayı** olmadan dövme fotoğrafını reklamda kullanma. Yüz görünüyorsa mutlaka onay al.
- `takip/musteri-takip.csv` dosyasında tam ad ve telefon tutma, **baş harfler** yeterli. Bu repo özel (private) kalmalı.
- Meta'ya müşteri listesi yükleyeceksen (hariç tutma kitlesi), müşterilerin bunu bildiğinden emin ol.

## 5. Ticari elektronik ileti (6563 sayılı Kanun / İYS)
- Müşteri sana yazdıysa, o konuşmayı sürdürmek ve takip etmek serbest.
- **Toplu kampanya mesajı** (SMS, e-posta, yayın listesi) için **önceden onay** gerekir. İşletmeler için **İYS** kaydı gündeme gelir. → 07'deki "Duyuru-Onaylı" etiket yöntemini kullan.

## 6. Vergi ve ücretler
- **Meta konum ücreti (Türkiye):** %5, faturada ayrı satır. 2026'da başladı (kaynaklar 1 Temmuz ve 1 Ekim diye çelişiyor).
- **Dijital Hizmet Vergisi:** 2026'da %5, 2027'de %2,5 (platformun ödediği vergi).
- **KDV:** Yurt dışından alınan reklam hizmetinde 2 No.lu KDV beyannamesi gündeme gelir. **Stopaj** konusunda kaynaklar net değil. → **Muhasebecine sor**, Meta ve Google faturalarını her ay ilet.

## 7. Google
- İşletme Profili adına anahtar kelime ekleme (askıya alma riski).
- Yorum satın alma veya teşvikli yorum yasak.
- Google Ads'te dövme hizmeti reklamı genel olarak serbest. Yetişkin içerik kurallarına (çıplaklık) dikkat et.

---
### Kaynaklar
- [T24 — 18 yaş altı dövme/piercing kanun teklifi](https://t24.com.tr/gundem/mhpli-karakoctan-18-yas-altina-dovme-ve-piercing-yapanlara-kasten-yaralama-duzenlemesi-teklifi,1304923)
- [Sözcü — Dövme ve piercinge hapis cezası teklifi](https://www.sozcu.com.tr/tbmm-ye-sunuldu-dovme-ve-piercinge-hapis-cezasi-kapida-p299445)
- [Memurlar.net — Bakanlık dövme yönergesi](https://www.memurlar.net/haber/67345/dovmeye-denetim-bakanlik-dovme-yonergesi-hazirladi.html)
- [Meta — Kozmetik işlemler politikası](https://transparency.meta.com/policies/ad-standards/content-specific-restrictions/cosmetic-procedures-and-wellness)
- [Stackmatix — Tattoo before/after ads & Meta policy](https://www.stackmatix.com/blog/tattoo-shop-before-after-ads-meta-policy)
- [LOG — Meta konum ücreti](https://www.log.com.tr/meta-platformlarinda-yayinlanan-reklamlardan-turkiye-dahil-bircok-ulkede-konum-ucreti-almaya-basliyor/)
- [Bianet — Dijital hizmet vergisi indirimi](https://bianet.org/haber/dijital-hizmet-vergisinde-indirim-314919)
- [Erdem & Erdem — Dijital reklam hizmetlerinde stopaj](https://www.erdem-erdem.av.tr/bilgi-bankasi/dijital-reklam-hizmetlerinde-stopaj-vergisi-sorunu)
