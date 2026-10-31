# Kurulum dosyaları

## Claude'u reklam hesaplarına bağlamak (MCP)
1. `mcp.ornek.json` dosyasını repo köküne **`.mcp.json`** adıyla kopyala:
   `cp kurulum/mcp.ornek.json .mcp.json`
2. **Meta (Pipeboard):** pipeboard.co'da hesap aç → Facebook reklam hesabını bağla. Claude Code ilk açılışta tarayıcıda giriş ister.
3. **Google Ads (resmi):**
   - Google Cloud'da proje aç → "Google Ads API"yi etkinleştir
   - Google Ads → Araçlar → API Merkezi → **geliştirici jetonu** al (Explorer erişimi yeterli)
   - `pipx` kur, sonra: `gcloud auth application-default login --scopes https://www.googleapis.com/auth/adwords,https://www.googleapis.com/auth/cloud-platform`
   - Ortam değişkenleri: `GOOGLE_APPLICATION_CREDENTIALS`, `GOOGLE_PROJECT_ID`, `GOOGLE_ADS_DEVELOPER_TOKEN`
4. Claude Code'u bu klasörde aç → sunucuları onayla → "Geçen haftanın reklam raporunu çıkar" de.

Ayrıntılar: `docs/09-acik-kaynak-araclar.md`

## n8n + Umami (isteğe bağlı, kendi sunucunda)
```bash
cp .env.ornek .env    # tüm değerleri değiştir
docker compose up -d
```
