# 07 · WhatsApp / DM Mesaj Scriptleri

> Reklam mesaj getirir, **randevuyu mesaj süreci getirir.** 100 mesajdan 10 randevu çıkarmakla 25 randevu çıkarmak arasındaki fark reklamda değil, bu sayfada.

## Altın kurallar
1. **Otomatik karşılama anında, insan cevabı ≤ 30 dk** (11:00–21:00). Karşılama mesajı müşteriyi oyalamaz; eleme sorularını sorar.
2. **Fiyatı saklama, aralık ver + soru sor.** "Fiyat için gelin" diyen kaybeder.
3. **Her mesajı bir soruyla bitir.** Konuşma ancak böyle ilerler.
4. **Sesli mesaj** at (30 sn): güveni hızla kurar. Sanatçının sesi çok etkilidir.
5. **Kodu kaydet:** Mesajın sonundaki `[K2-02]` → `takip/musteri-takip.csv` → `kaynak_kodu`.

## WhatsApp Business kurulumu (kurul tur 1 kararıyla güncellendi)
- **Karşılama mesajı** (otomatik, ilk mesajda; Erdem'in ağzından):
  > Merhaba, ben Erdem Melih 🖤 Mesajın bana ulaştı. Çalışma saatlerinde (11:00–21:00) genelde **30 dakika içinde** dönüyorum; seanstaysam biraz uzayabilir, ama mutlaka dönüyorum.
  > Hızlanmak için şunları gönderebilirsin:
  > 1️⃣ Fikrin ya da referans fotoğrafın
  > 2️⃣ Dövmenin yeri (kol, bacak, sırt…)
  > 3️⃣ Yaklaşık boyutu
  > 4️⃣ Hangi semttesin, ne zaman düşünüyorsun?
  > Fotoğrafı ve boyutu gönderirsen ilk cevabımda **yaklaşık fiyat aralığını ve seans sayısını** yazıyorum; net fiyat tasarım netleşince. Tasarım görüşmesi ücretsiz ve bağlayıcı değil. Kişisel verilerin: {kvkk_link}
- **Uzakta mesajı** (mesai dışı):
  > Şu an stüdyo kapalı. Mesajını aldım, yarın 11:00'den itibaren ilk iş sana dönüyorum. Bu arada işlerime bak: instagram.com/{instagram}
- **Etiketler:** 🟡 Yeni · 🟠 Ciddi talep · 🔵 Fiyat verildi · 🟢 Kapora alındı · 🟣 Randevu · ✅ Tamamlandı · ⭐ Yorum istendi · ⚪ Kayıp · 📣 Duyuru-Onaylı
- **"Ciddi talep" tanımı (rapor için):** Bölgesini, yaklaşık boyutunu ve fikrini/referansını paylaşan VE tasarım görüşmesi ya da fiyat aşamasına gelen kişi. Sadece bunlar `takip/musteri-takip.csv`'ye yazılır.
- **Kod:** Mesajın sonundaki (R1), (C1), (F5)… → takip dosyasında `kaynak_kodu`. Kod yoksa WhatsApp sohbetin üstündeki "reklamdan geldi" kartına bak.
- **Hızlı yanıtlar** (`/` ile çağrılır): aşağıdaki şablonları `/fiyat`, `/portre`, `/kapora`, `/bakim`, `/yorum` olarak kaydet.
- **Seans sırasında mesajlar:** Kimin bakacağı (ya da hangi molalarda bakılacağı) sahibince yazılı belirlenir: `kurul/plan-v3.md` yayın kapısı.

---

## Şablonlar

### /ilk: İlk cevap (fikir geldiğinde)
> Çok güzel bir fikir! 😊 Netleştirmek için 3 kısa soru:
> 1️⃣ Vücudun neresine düşünüyorsun?
> 2️⃣ Yaklaşık kaç cm olsun (ya da avuç içi / parmak boyu gibi)?
> 3️⃣ İlk dövmen mi?
> Bunlara göre sana net fiyat ve tasarım önerisi yapacağım.

### /fiyat: Fiyat verirken
> Bu boyut ve detayda yaklaşık **{X}–{Y} TL**, **{N} seans** olur; net fiyatı tasarım netleşince yazılı veriyorum. Tasarım sana özel çiziliyor, tek kullanımlık iğne ve sterilize ekipman kullanıyoruz, iyileşme sürecinde takipteyiz.
> Bu hafta {gün1} veya {gün2} müsaitim. Hangisi sana uyar?

### /portre: Portre talebi geldiğinde
> Çok kıymetli bir fikir 🖤 Fotoğrafını (varsa birkaç farklı fotoğraf) gönder; netliğine, ışığına ve açısına bakıp sana **dürüstçe** söyleyeyim. Portrede benzerlik büyük ölçüde referans fotoğrafın kalitesine bağlı. Yaptığım portrelerden örnekleri de gönderiyorum.
> Nereye ve yaklaşık hangi boyutta düşünüyorsun?

*Not (müşteriye gönderilmez):* Onaylı gerçek-kişi portre örneği yoksa şunu de: "Gerçek kişi portrelerimi müşteri gizliliği nedeniyle paylaşmıyorum; benzer detay seviyesindeki işlerimi gösteriyorum." Kesin benzerlik ya da "birebir aynı" sözü verme.

### /pahali: "Pahalı" itirazı
> Haklısın, en ucuzu biz değiliz 🙂 Dövme ömür boyu seninle kalıyor. O yüzden sterilize ekipman, temiz çizgi ve iyileşme takibine yatırım yapıyoruz. İstersen boyutu biraz küçültüp {Y} TL'ye uyarlayabilirim, ya da tasarımı sadeleştirebiliriz. Hangisi daha çok içine siner?

### /dusunecegim: "Düşüneceğim"
> Tabii, acelesi yok! Kafandaki soru acı mı, fiyat mı, yoksa tasarım mı? Söylersen yardımcı olayım. Bu arada benzer işlerimden birkaçını atıyorum 👇

### /kapora: Kapora
> Harika! Randevunu kesinleştirmek için **{kapora} TL** kapora alıyoruz. Tasarım çizimi kaporayla başlar. Bu tutar toplam fiyattan düşülüyor. IBAN: {IBAN} (Açıklamaya adını yaz). Kapora gelince tasarım çizimine başlıyorum, randevudan 1 gün önce çizimi sana atacağım ✍️
> Not: 18 yaşından küçüklere dövme yapmıyoruz, randevuya **kimliğini** getirmeyi unutma.

> **İade/erteleme:** [SAHİP YAZACAK, örn. "Randevudan en az 48 saat önce haber verirsen kaporan yeni tarihe aktarılır; tasarım çizildikten sonra iade edilmez."] ⚠️ Bu satır doldurulmadan ilk kapora alınmaz (yayın kapısı).

### /hatirlatma: Randevudan 1 gün önce
> Yarın saat {saat}'te görüşüyoruz! 🖤 Hazırlık:
> • Gece iyi uyu, gelmeden önce yemek ye
> • Alkol alma (24 saat)
> • Dövme yapılacak bölgeye rahat ulaşılacak kıyafet giy
> • Kimliğini getir
> 📍 Konum: {google_maps_link}

### /bakim: Seans sonrası
> Ellerine sağlık, harika bir seanstı! İlk 14 gün için kısa bakım rehberi: (bakım görselini gönder). Takıldığın her şeyi buradan sor. 4 hafta sonra iyileşmiş halinin bir fotoğrafını atarsan çok sevinirim 📸

### /yorum: Yorum isteği (seans sonrası + 4. hafta)
> Memnun kaldıysan Google'a bırakacağın kısa bir yorum bizim için çok değerli 🙏 Bahçeşehir'de bizi bulmak isteyenlere yol gösteriyor:
> {google_yorum_linki}

### /takip1: Takip 1 (fiyat verildi, 2 gün ses yok)
> Selam! Geçen gün konuştuğumuz {stil} dövme için bu hafta {gün} günü bir boşluğum açıldı. Ayırmamı ister misin? 🙂

### /takip2: Takip 2 (7 gün sonra, son)
> Merhaba! Fikrin hâlâ aklındaysa buradayım. Değilse de hiç sorun değil 🖤 İleride istersen bu mesajı bulman yeterli.
> (Bundan sonra kampanya mesajı atma, bkz. izin kuralı ↓)

---

## ⚠️ İzin kuralı (6563 sayılı Kanun / İYS)
- Müşteri **sana yazdıysa** ve o konuşma içinde cevap verip takip ediyorsan sorun yok.
- **Toplu kampanya / indirim mesajı** (yayın listesi, SMS) atmak için müşterinin **önceden onayı** gerekir. İşletmeler için **İYS (İleti Yönetim Sistemi)** kaydı gündeme gelir. Toplu mesaj atmadan önce muhasebecine sor.
- Pratik çözüm: Seans sonunda "Kampanya ve flash günü duyurularını WhatsApp'tan almak ister misin?" diye sor. "Evet" diyenleri **"Duyuru-Onaylı"** etiketiyle işaretle. Yayın listesine sadece onları ekle.
