# 09 · GitHub'dan İşe Yarayan Açık Kaynak Araçlar

Seçim kriterleri: **aktif geliştirilen** (Ekim 2026'da güncellenmiş), **yaygın kullanılan** ve **dövme stüdyosunun gerçek bir sorununu çözen** projeler. Yıldız sayıları 31 Ekim 2026 itibarıyla.

## ⭐ Öncelik sırası (ne zaman neyi kur?)

| Sıra | Araç | Sorun | Zorluk |
|---|---|---|---|
| 1 | **Claude + Meta/Google MCP** | Reklamları sohbetten yönet ve raporla | Kolay |
| 2 | **Postiz** | Reels ve gönderileri haftalık planla, tek yerden IG + TikTok + FB | Orta |
| 3 | **Umami** | Landing sayfası ziyaret ve UTM analizi | Orta |
| 4 | **n8n** | Otomasyon: yeni WhatsApp talebini tabloya yaz, 2 gün sonra hatırlat | Orta-zor |
| 5 | **Chatwoot** | IG DM + WhatsApp + Facebook tek gelen kutusunda (birden fazla sanatçı varsa) | Zor |
| — | Cal.com / Easy!Appointments | Online randevu takvimi | Orta |

---

## 1. Reklam hesabını Claude'a bağlamak (MCP)
"Reklam yöneticin olayım" dedin. Bunun için Claude'un hesabı **görmesi** gerekiyor.

**a) En kolay yol: Claude'daki AdsAgent eklentisi.** Bu oturumda AdsAgent'ın Meta, Google ve TikTok bağlantıları yüklü ama **yetkilendirilmemiş**. claude.ai → Ayarlar → Connectors (Bağlayıcılar) bölümünden yetki verirsen performans okuma, kampanya kurma ve bütçe değiştirme işlerini sohbetten yaparım. Her yazma işleminden önce sana onay sorarım.

**b) Açık kaynak MCP sunucuları** (Claude Code'da bu repo açıkken):

| Proje | Ne yapar | Yıldız |
|---|---|---|
| [googleads/google-ads-mcp](https://github.com/googleads/google-ads-mcp) | **Google'ın resmi** MCP'si: hesap ve kampanya verisini okur (GAQL ile). Yazma yok. | ~1.1k |
| [pipeboard-co/meta-ads-mcp](https://github.com/pipeboard-co/meta-ads-mcp) | Meta reklamları: okuma + kampanya/set/reklam oluşturma (varsayılan PAUSED), bütçe güncelleme. Barındırılan hizmet, ücretsiz planı var. | ~1.3k |

Kurulum: `kurulum/mcp.ornek.json` dosyasını repo köküne `.mcp.json` adıyla kopyala, ortam değişkenlerini ayarla. Claude Code açılınca onay ister.

> ⚠️ Pipeboard üçüncü taraf bir hizmettir: reklam hesabına erişim verirsin. Resmi Meta iş ortağı olduğunu belirtiyor. Kullanmadan önce gizlilik koşullarını oku.

## 2. Resmi reklam SDK'ları (bu repodaki scriptler bunları kullanıyor)
| Proje | Kullanım | Yıldız |
|---|---|---|
| [meta/facebook-python-business-sdk](https://github.com/meta/facebook-python-business-sdk) | `tools/meta_kur.py`: kampanyaları API ile kurar | ~1.6k |
| [googleads/google-ads-python](https://github.com/googleads/google-ads-python) | Google Ads API (ileride otomatik rapor için) | ~760 |
| [Brainlabs-Digital/Google-Ads-Scripts](https://github.com/Brainlabs-Digital/Google-Ads-Scripts) | Google Ads içine yapıştırılan hazır scriptler (bütçe takibi, arama terimi analizi) | ~160 |

## 3. Sosyal medya planlama
| Proje | Neden | Yıldız |
|---|---|---|
| [gitroomhq/postiz-app](https://github.com/gitroomhq/postiz-app) | Instagram, TikTok, Facebook, YouTube… Tek takvimde planla, yapay zekâ ile metin önerisi. Kendi sunucunda ya da bulut sürümünde. | ~40k |
| [inovector/mixpost](https://github.com/inovector/mixpost) | Daha sade bir Buffer alternatifi (Laravel/PHP) | ~3.9k |

## 4. Müşteri iletişimi ve otomasyon
| Proje | Neden | Yıldız |
|---|---|---|
| [n8n-io/n8n](https://github.com/n8n-io/n8n) | Görsel otomasyon. Örnek: "Yeni Meta lead → Google Sheets'e yaz → 48 saat sonra hatırlat" | ~209k |
| [chatwoot/chatwoot](https://github.com/chatwoot/chatwoot) | IG DM, WhatsApp (resmi Cloud API), web chat: tek gelen kutusu, etiketler, ekip ataması | ~39k |
| [twentyhq/twenty](https://github.com/twentyhq/twenty) | Açık kaynak CRM. Müşteri sayısı 500'ü geçince CSV yerine kullanılabilir. | ~60k |

> ⚠️ **WhatsApp uyarısı:** GitHub'da "WhatsApp Web API" projeleri çok (Evolution API, OpenWA vb.). Bunlar **resmi olmayan** yollarla çalışır. Toplu mesajda **numaranın kapatılma riski** var. İşletme numaran için sadece **resmi WhatsApp Business uygulamasını** veya **WhatsApp Cloud API**'yi (Chatwoot/n8n ile) kullan.

## 5. Analitik ve randevu
| Proje | Neden | Yıldız |
|---|---|---|
| [umami-software/umami](https://github.com/umami-software/umami) | Çerezsiz, KVKK dostu web analitiği. UTM kampanya raporu var. | ~40k |
| [alextselegidis/easyappointments](https://github.com/alextselegidis/easyappointments) | Basit online randevu sistemi, Google Takvim senkronu | ~4.5k |
| [calcom/cal.com](https://github.com/calcom/cal.com) | Gelişmiş randevu altyapısı (bulut sürümü ücretsiz başlar) | — |

> Dövmede randevu genelde konuşarak alınır, o yüzden **online takvim şart değil**. Danışma görüşmesi için 15 dakikalık Cal.com linki işe yarayabilir.

## Kendi sunucunda çalıştırmak (isteğe bağlı)
`kurulum/docker-compose.yml` dosyası **n8n + Umami**'yi tek komutla ayağa kaldırır (aylık ~5 $'lık bir VPS yeterli):
```bash
cd kurulum && cp .env.ornek .env   # şifreleri değiştir
docker compose up -d
# n8n → http://SUNUCU:5678   Umami → http://SUNUCU:3000
```

## Bilerek EKLEMEDİKLERİM
- **Yıldız sayısı kısa sürede şişmiş "ücretsiz alternatif" repolar**: bazıları ücretli hizmetlerin reklam vitrini.
- **Instagram bot / otomatik takip-beğeni** araçları: Instagram yasaklıyor, hesabın kapanabilir.
- **Resmi olmayan WhatsApp toplu mesaj** araçları: numara kapanma riski + İYS/izin sorunu.
