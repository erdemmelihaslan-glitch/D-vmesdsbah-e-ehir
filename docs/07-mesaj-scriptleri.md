# 07 · WhatsApp / DM Mesaj Scriptleri

> Reklam mesaj getirir, **randevuyu mesaj süreci getirir.** 100 mesajdan 10 randevu çıkarmakla 25 randevu çıkarmak arasındaki fark reklamda değil, bu sayfada.

## Altın kurallar
1. **5 dakika içinde cevap ver.** 1 saat sonra müşteri başka stüdyoya yazmış olur.
2. **Fiyatı saklama, aralık ver + soru sor.** "Fiyat için gelin" diyen kaybeder.
3. **Her mesajı bir soruyla bitir.** Konuşma ancak böyle ilerler.
4. **Sesli mesaj** at (30 sn): güveni hızla kurar. Sanatçının sesi çok etkilidir.
5. **Kodu kaydet:** Mesajın sonundaki `[K2-02]` → `takip/musteri-takip.csv` → `kaynak_kodu`.

## WhatsApp Business kurulumu
- **Karşılama mesajı** (otomatik, ilk mesajda):
  > Merhaba, {studyo_adi}'na hoş geldin! 🖤 Ben {sanatci}. Aklındaki dövmenin bir fotoğrafını ya da fikrini, istediğin yeri ve yaklaşık boyutu yazarsan sana hemen dönüyorum.
- **Uzakta mesajı** (mesai dışı):
  > Şu an seanstayım ya da stüdyo kapalı. Mesajını aldım, ilk fırsatta (genelde 1 saat içinde) dönüyorum. Bu arada işlerime bak: instagram.com/{instagram}
- **Etiketler:** 🟡 Yeni · 🔵 Fiyat verildi · 🟢 Kapora alındı · 🟣 Randevu · ✅ Tamamlandı · ⭐ Yorum istendi · ⚪ Kayıp
- **Hızlı yanıtlar** (`/` ile çağrılır): aşağıdaki şablonları `/fiyat`, `/kapora`, `/bakim`, `/yorum` olarak kaydet.

---

## Şablonlar

### /ilk: İlk cevap (fikir geldiğinde)
> Çok güzel bir fikir! 😊 Netleştirmek için 3 kısa soru:
> 1️⃣ Vücudun neresine düşünüyorsun?
> 2️⃣ Yaklaşık kaç cm olsun (ya da avuç içi / parmak boyu gibi)?
> 3️⃣ İlk dövmen mi?
> Bunlara göre sana net fiyat ve tasarım önerisi yapacağım.

### /fiyat: Fiyat verirken
> Bu boyut ve detayda fiyatı **{X} TL** olur. Tasarım sana özel çiziliyor, tek kullanımlık iğne ve steril ekipman kullanıyoruz, iyileşme sürecinde takipteyiz, gerekirse rötuşu ücretsiz yapıyoruz.
> Bu hafta {gün1} veya {gün2} müsaitim. Hangisi sana uyar?

### /pahali: "Pahalı" itirazı
> Haklısın, en ucuzu biz değiliz 🙂 Dövme ömür boyu seninle kalıyor. O yüzden steril ortam, temiz çizgi ve iyileşme takibine yatırım yapıyoruz. İstersen boyutu biraz küçültüp {Y} TL'ye uyarlayabilirim, ya da tasarımı sadeleştirebiliriz. Hangisi daha çok içine siner?

### /dusunecegim: "Düşüneceğim"
> Tabii, acelesi yok! Kafandaki soru acı mı, fiyat mı, yoksa tasarım mı? Söylersen yardımcı olayım. Bu arada benzer işlerimden birkaçını atıyorum 👇

### /kapora: Kapora
> Harika! Randevunu kesinleştirmek için **{kapora} TL** kapora alıyoruz. Bu tutar toplam fiyattan düşülüyor. IBAN: {IBAN} (Açıklamaya adını yaz). Kapora gelince tasarım çizimine başlıyorum, randevudan 1 gün önce çizimi sana atacağım ✍️
> Not: 18 yaşından küçüklere dövme yapmıyoruz, randevuya **kimliğini** getirmeyi unutma.

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
