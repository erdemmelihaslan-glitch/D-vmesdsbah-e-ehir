#!/usr/bin/env python3
"""Reklam kreatiflerini üretir (fotoğraf + video): v2, kurul tur 1 kararlarıyla.

    python3 tools/kreatif_uret.py                       # hepsi, 1080p
    python3 tools/kreatif_uret.py --sadece foto
    python3 tools/kreatif_uret.py --sadece video --muzik parca.mp3   # Meta Ses Koleksiyonu'ndan
    python3 tools/kreatif_uret.py --cozunurluk 4k       # 4K ana kopyalar → kreatif/cikti_4k/

Girdi : kreatif/kaynak/ (orijinal foto/video) + kreatif/kreatif.yaml
Çıktı : kreatif/cikti/{akis_4x5, hikaye_9x16, carousel, video}

Kurallar (kurul kararı):
- Dövmenin kendisi rötuşlanmaz. Sadece kadraj, global gamma, arka plan temizliği, format, yazı.
- Yapay zekâ ile büyütme yok. Kaynaktan en fazla 1,5x büyütülür (4K için orijinal dosya gerekir).
- 9:16'da yazı ve logo yüksekliğin %14–65'i arasında kalır (Reels arayüzü altta ~%35).
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

import numpy as np
import yaml
from PIL import Image, ImageDraw, ImageFilter, ImageFont

KOK = Path(__file__).resolve().parent.parent
KAYNAK = KOK / "kreatif" / "kaynak"
CIKTI = KOK / "kreatif" / "cikti"
FONT_DIR = Path("/usr/share/fonts/opentype/inter")
FPS = 30
KEMIK = (237, 231, 221)
GRI = (176, 170, 162)
SIYAH = (6, 6, 7)
S = 1            # ölçek: 1 = 1080p, 2 = 4K
M: dict = {}     # marka
ISL: dict = {}   # işleme ayarları
UYARILAR: list[str] = []


def u(x: float) -> int:
    return int(round(x * S))


def font(ad: str, boy: float) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(str(FONT_DIR / ad), u(boy))
    except OSError:
        return ImageFont.truetype("DejaVuSans-Bold.ttf" if ("Bold" in ad or "Black" in ad) else "DejaVuSans.ttf", u(boy))


def tr_buyuk(s: str) -> str:
    return s.replace("i", "İ").replace("ı", "I").upper()


# ---------------------------------------------------------------- metin yardımcıları
def genislik(metin, f, aralik=0):
    return sum(f.getlength(c) for c in metin) + aralik * max(0, len(metin) - 1)


def yaz_orta(d, x, y, metin, f, renk, aralik=0):
    x = x - genislik(metin, f, aralik) / 2
    for c in metin:
        d.text((x, y), c, font=f, fill=renk)
        x += f.getlength(c) + aralik


def satir_bol(metin, f, max_g):
    satirlar, s = [], ""
    for k in metin.split():
        dene = (s + " " + k).strip()
        if f.getlength(dene) <= max_g:
            s = dene
        else:
            satirlar.append(s)
            s = k
    satirlar.append(s)
    return satirlar


def katman(boyut, ciz, golge=True):
    k = Image.new("RGBA", boyut, (0, 0, 0, 0))
    ciz(ImageDraw.Draw(k))
    if not golge:
        return k
    g = Image.new("RGBA", boyut, (0, 0, 0, 0))
    g.putalpha(k.getchannel("A").filter(ImageFilter.GaussianBlur(u(10))).point(lambda a: int(a * 0.85)))
    return Image.alpha_composite(g, k)


def scrim(boyut, ust: bool, yukseklik, guc=0.85):
    w, h = boyut
    a = np.zeros((h, w), dtype=np.uint8)
    ramp = (np.linspace(1, 0, yukseklik) ** 1.6 * 255 * guc).astype(np.uint8)
    if ust:
        a[:yukseklik] = ramp[:, None]
    else:
        a[h - yukseklik:] = ramp[::-1][:, None]
    s = Image.new("RGBA", boyut, (0, 0, 0, 255))
    s.putalpha(Image.fromarray(a))
    return s


def ustune(taban: Image.Image, *katmanlar) -> Image.Image:
    t = taban.convert("RGBA")
    for k in katmanlar:
        t = Image.alpha_composite(t, k)
    return t.convert("RGB")


# ---------------------------------------------------------------- fotoğraf işleme
def foto_yukle(oge: dict) -> Image.Image:
    im = Image.open(KAYNAK / oge["dosya"]).convert("RGB")
    for x1, y1, x2, y2 in oge.get("temizle", []):
        a = np.asarray(im).copy()
        p = 30
        cev = np.concatenate([
            a[max(0, y1 - p):y1, x1:x2].reshape(-1, 3), a[y2:y2 + p, x1:x2].reshape(-1, 3),
            a[y1:y2, max(0, x1 - p):x1].reshape(-1, 3), a[y1:y2, x2:x2 + p].reshape(-1, 3)])
        a[y1:y2, x1:x2] = np.median(cev, axis=0).astype(np.uint8)
        maske = Image.new("L", im.size, 0)
        ImageDraw.Draw(maske).rectangle([x1 - 6, y1 - 6, x2 + 6, y2 + 6], fill=255)
        im = Image.composite(Image.fromarray(a), im, maske.filter(ImageFilter.GaussianBlur(5)))
    if oge.get("kirp"):
        im = im.crop(tuple(oge["kirp"]))
    g = ISL["gamma"]   # global gamma: siyah (0) ve beyaz (255) sabit, orta tonlar açılır
    lut = [round(255 * ((i / 255) ** (1 / g))) for i in range(256)]
    return im.point(lut * 3)


def bulanik_zemin(im, boyut):
    w, h = boyut
    o = max(w / im.width, h / im.height)
    z = im.resize((int(im.width * o) + 2, int(im.height * o) + 2), Image.BICUBIC)
    z = z.crop(((z.width - w) // 2, (z.height - h) // 2, (z.width - w) // 2 + w, (z.height - h) // 2 + h))
    z = z.filter(ImageFilter.GaussianBlur(u(45)))
    return Image.eval(z, lambda v: int(v * ISL["zemin_parlaklik"]))


def yumusak_yapistir(c, p, x, y, kenar=None):
    kenar = kenar or u(70)
    m = np.ones((p.height, p.width), dtype=np.float32)
    r = np.linspace(0, 1, kenar, dtype=np.float32)
    if y > 0:
        m[:kenar] *= r[:, None]
    if y + p.height < c.height:
        m[-kenar:] *= r[::-1][:, None]
    if x > 0:
        m[:, :kenar] *= r[None, :]
    if x + p.width < c.width:
        m[:, -kenar:] *= r[None, ::-1]
    c.paste(p, (x, y), Image.fromarray((m * 255).astype(np.uint8)))


def doldur(im, oge, W, H, merkez_y=None):
    """Dövmeyi kadraja DOLDURUR (dövme genişliğin ~%60'ı). Büyütme ≤ max_buyutme.
    Döner: (tuval, kaynak→tuval koordinat dönüştürücü)."""
    cx, cy = oge.get("odak", (im.width / 2, im.height / 2))
    gen = oge.get("dovme_gen", im.width * 0.6)
    oran = W / H
    cap = ISL["max_buyutme"]
    cw = min(max(gen / ISL["dovme_orani"], W / cap), im.width)
    ch = cw / oran
    if ch > im.height:
        ch = im.height
        cw = min(im.width, ch * oran)
    s = min(W / cw, H / ch, cap)
    if s >= cap - 1e-6 and (cw * s < W - 2 or ch * s < H - 2):
        UYARILAR.append(f"{oge['kod']}: kaynak çözünürlüğü bu format için yetersiz ({im.width}px) → orijinal dosya gerekli")
    x0 = min(max(cx - cw / 2, 0), im.width - cw)
    y0 = min(max(cy - ch / 2, 0), im.height - ch)
    p = im.crop((round(x0), round(y0), round(x0 + cw), round(y0 + ch))).resize((round(cw * s), round(ch * s)), Image.LANCZOS)
    if s <= 1.2:
        p = p.filter(ImageFilter.UnsharpMask(radius=1.2 * S, percent=25, threshold=3))
    c = bulanik_zemin(im, (W, H))
    my = merkez_y if merkez_y is not None else H / 2
    px = (W - p.width) // 2
    py = int(min(max(my - p.height / 2, 0), H - p.height))
    yumusak_yapistir(c, p, px, py)
    return c, (lambda x, y: (px + (x - x0) * s, py + (y - y0) * s))


# ---------------------------------------------------------------- tasarım parçaları
def imza(d, W, y):
    yaz_orta(d, W / 2, y, tr_buyuk(M["ust"]), font("InterDisplay-Bold.otf", 36), KEMIK, u(9))
    yaz_orta(d, W / 2, y + u(48), M["alt"], font("Inter-Medium.otf", 24), GRI, u(8))


def teklif_etiketi(boyut, y, metin=None):
    """Yarı saydam koyu zemin üstünde teklif satırı (görselde okunur)."""
    metin = metin or M["teklif"]
    f = font("Inter-SemiBold.otf", 40)
    W = boyut[0]
    k = Image.new("RGBA", boyut, (0, 0, 0, 0))
    d = ImageDraw.Draw(k)
    w = genislik(metin, f) + u(64)
    d.rounded_rectangle([W / 2 - w / 2, y, W / 2 + w / 2, y + u(76)], radius=u(38), fill=(0, 0, 0, 165))
    yaz_orta(d, W / 2, y + u(14), metin, f, KEMIK)
    return k


def akis_4x5(im, oge):
    W, H = u(1080), u(1350)
    c, _ = doldur(im, oge, W, H)
    return ustune(c, scrim((W, H), False, u(300)), katman((W, H), lambda d: imza(d, W, H - u(122))))


def hikaye_9x16(im, oge, yazi):
    """Story/Reels görseli. Tüm yazılar y=%14–65 bandında (269–1248 px)."""
    W, H = u(1080), u(1920)
    c, _ = doldur(im, oge, W, H, merkez_y=u(860))

    def ciz(d):
        f = font("InterDisplay-Bold.otf", 66)
        for i, s in enumerate(satir_bol(yazi, f, u(940))):
            yaz_orta(d, W / 2, u(300) + i * u(80), s, f, KEMIK)
        imza(d, W, u(1062))
    return ustune(c, scrim((W, H), True, u(600), 0.8), katman((W, H), ciz), teklif_etiketi((W, H), u(1160)))


def kapanis_karti(W, H, mod="reklam", baslik=None, alt=None, uzmanlik=None):
    """mod: 'reklam' (teklif + çağrı) | 'organik' (sadece marka). İçerik y=470–1100 arasında."""
    c = Image.new("RGB", (W, H), SIYAH)
    d = ImageDraw.Draw(c)
    if baslik:
        fb = font("InterDisplay-Bold.otf", 60)
        sat = satir_bol(baslik, fb, W - u(160))
        for i, s in enumerate(sat):
            yaz_orta(d, W / 2, u(220) + i * u(72), s, fb, KEMIK)
        if alt:
            yaz_orta(d, W / 2, u(220) + len(sat) * u(72) + u(18), alt, font("Inter-Regular.otf", 32), GRI)
    d.line([(W / 2 - u(40), u(470)), (W / 2 + u(40), u(470))], fill=GRI, width=max(2, u(2)))
    yaz_orta(d, W / 2, u(500), tr_buyuk(M["ust"]), font("InterDisplay-Bold.otf", 84), KEMIK, u(14))
    yaz_orta(d, W / 2, u(608), M["alt"], font("Inter-Medium.otf", 28), GRI, u(14))
    yaz_orta(d, W / 2, u(690), uzmanlik or M["uzmanlik"], font("Inter-Regular.otf", 40), KEMIK)
    if mod == "reklam":
        yaz_orta(d, W / 2, u(790), M["teklif"], font("Inter-SemiBold.otf", 40), KEMIK)
        fc = font("Inter-Medium.otf", 34)
        cw = genislik(M["cta"], fc) + u(72)
        d.rounded_rectangle([W / 2 - cw / 2, u(880), W / 2 + cw / 2, u(956)], radius=u(38),
                            outline=KEMIK, width=max(2, u(2)))   # ince çerçeve (sahte buton değil)
        yaz_orta(d, W / 2, u(897), M["cta"], fc, KEMIK)
    yaz_orta(d, W / 2, u(1030), f"{M['konum']}   ·   {M['hesap']}", font("Inter-Medium.otf", 28), GRI)
    return c


# ---------------------------------------------------------------- video
class Yazici:
    def __init__(self, yol: Path, sure: float, ses: Path | None = None, muzik: Path | None = None):
        W, H = u(1080), u(1920)
        k = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
             "-r", str(FPS), "-i", "-"]
        if muzik:
            k += ["-i", str(muzik), "-map", "0:v", "-map", "1:a",
                  "-af", f"afade=t=in:d=0.3,afade=t=out:st={max(0, sure - 0.6):.2f}:d=0.6"]
        elif ses:
            k += ["-i", str(ses), "-map", "0:v", "-map", "1:a", "-af", "apad"]
        else:
            k += ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-map", "0:v", "-map", "1:a"]
        k += ["-t", f"{sure:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
              "-profile:v", "high", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(yol)]
        self.p = subprocess.Popen(k, stdin=subprocess.PIPE)
        self.n = 0

    def yaz(self, im):
        self.p.stdin.write(im.convert("RGB").tobytes())
        self.n += 1

    def kapat(self):
        self.p.stdin.close()
        if self.p.wait() != 0:
            raise SystemExit("ffmpeg hatası")


def video_kareleri(yol: Path, n: int):
    """Kaynak videoyu 9:16 / 30 fps okur. Büyütülmüş kaynakta netleştirme YOK (kurul kararı)."""
    W, H = u(1080), u(1920)
    vf = (f"fps=30,scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},"
          "eq=contrast=1.03")
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(yol), "-vf", vf, "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    boy = W * H * 3
    try:
        for _ in range(n):
            b = p.stdout.read(boy)
            if len(b) < boy:
                break
            yield Image.frombytes("RGB", (W, H), b)
    finally:
        p.kill()
        p.wait()


def yakinlas(c, z, mx, my):
    W, H = c.size
    w, h = W / z, H / z
    x = min(max(mx - w / 2, 0), W - w)
    y = min(max(my - h / 2, 0), H - h)
    return c.resize((W, H), Image.BICUBIC, box=(x, y, x + w, y + h))


def ust_yazi(metin, alt=None, boy=84):
    W, H = u(1080), u(1920)

    def ciz(d):
        f = font("InterDisplay-Black.otf", boy)
        sat = satir_bol(metin, f, u(960))
        for i, s in enumerate(sat):
            yaz_orta(d, W / 2, u(300) + i * u(boy + 12), s, f, KEMIK)
        if alt:
            yaz_orta(d, W / 2, u(300) + len(sat) * u(boy + 12) + u(16), alt, font("Inter-SemiBold.otf", 44), KEMIK, u(2))
    return Image.alpha_composite(scrim((W, H), True, u(640), 0.8), katman((W, H), ciz))


def video_sure(yol):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(yol)],
                         capture_output=True, text=True).stdout
    return float(out)


def r1_uret(V, fotolar, ogeler, muzik):
    W, H = u(1080), u(1920)
    n_ac, n_cek, n_kes, n_kap = 60, 36, int(V["kesme_suresi"] * FPS), int(V["kapanis_suresi"] * FPS)
    toplam = n_ac + n_kes * len(V["kesmeler"]) + n_kap
    y = Yazici(CIKTI / "video" / V["cikti"], toplam / FPS, muzik=muzik)
    acilis = ogeler[V["acilis"]]
    c, harita = doldur(fotolar[V["acilis"]], acilis, W, H, merkez_y=u(860))
    gx, gy = harita(*acilis.get("goz", acilis["odak"]))
    k1, k2 = ust_yazi(V["kanca"]), ust_yazi(V["kanca2"], V.get("kanca2_alt"))
    for i in range(n_ac):                       # 0–1,2 sn: gözlerden geri çekil · 1,2–2,0 sn: tut
        if i < n_cek:
            e = 1 - (1 - i / (n_cek - 1)) ** 3
            kare = yakinlas(c, 1.8 + (1.0 - 1.8) * e, gx + (W / 2 - gx) * e, gy + (H / 2 - gy) * e)
            y.yaz(ustune(kare, k1))
        else:
            y.yaz(ustune(c, k2))
    for kod in V["kesmeler"]:                    # sert kesmeler, vuruşa oturur
        ck, _ = doldur(fotolar[kod], ogeler[kod], W, H, merkez_y=u(860))
        for i in range(n_kes):
            y.yaz(yakinlas(ck, 1.0 + 0.04 * i / max(1, n_kes - 1), W / 2, H / 2))
    kap = kapanis_karti(W, H)
    for _ in range(n_kap):
        y.yaz(kap)
    y.kapat()
    return y.n


def r2_uret(V, fotolar, ogeler, muzik):
    W, H = u(1080), u(1920)
    kay = KAYNAK / V["kaynak"]
    n_vid = int(video_sure(kay) * FPS) - 2
    n_son, n_kap = int(V["sonuc_suresi"] * FPS), int(V["kapanis_suresi"] * FPS)
    y = Yazici(CIKTI / "video" / V["cikti"], (n_vid + n_son + n_kap) / FPS, muzik=muzik)
    k1 = ust_yazi(V["kanca"])
    kare = None
    for i, kare in enumerate(video_kareleri(kay, n_vid)):
        y.yaz(ustune(kare, k1) if i < 78 else kare)
    while y.n < n_vid:  # kaynak kısa kalırsa son kareyi tut
        y.yaz(kare)
    c, _ = doldur(fotolar[V["sonuc_foto"]], ogeler[V["sonuc_foto"]], W, H, merkez_y=u(880))
    k2 = ust_yazi(V["sonuc_yazi"], V.get("sonuc_alt"))
    for i in range(n_son):
        y.yaz(ustune(yakinlas(c, 1.0 + 0.05 * i / (n_son - 1), W / 2, u(880)), k2))
    kap = kapanis_karti(W, H, uzmanlik="Realizm dövme")
    for _ in range(n_kap):
        y.yaz(kap)
    y.kapat()
    return y.n


def organik_uret(V):
    W, H = u(1080), u(1920)
    kay = KAYNAK / V["kaynak"]
    n_vid = int(video_sure(kay) * FPS) - 2
    n_kap = 60
    y = Yazici(CIKTI / "video" / V["cikti"], (n_vid + n_kap) / FPS, ses=kay)
    kare = None
    for kare in video_kareleri(kay, n_vid):
        y.yaz(kare)
    while y.n < n_vid:
        y.yaz(kare)
    kap = kapanis_karti(W, H, mod="organik")
    for _ in range(n_kap):
        y.yaz(kap)
    y.kapat()
    return y.n


# ---------------------------------------------------------------- ana akış
def main():
    global S, CIKTI, M, ISL
    ap = argparse.ArgumentParser()
    ap.add_argument("--sadece", choices=["foto", "video"])
    ap.add_argument("--cozunurluk", choices=["1080", "4k"], default="1080")
    ap.add_argument("--muzik", type=Path, help="Meta Ses Koleksiyonu'ndan indirilen parça (mp3/wav)")
    a = ap.parse_args()
    if a.cozunurluk == "4k":
        S, CIKTI = 2, KOK / "kreatif" / "cikti_4k"
    K = yaml.safe_load((KOK / "kreatif" / "kreatif.yaml").read_text(encoding="utf-8"))
    M, ISL = K["marka"], K["isleme"]
    ogeler = {o["kod"]: o for o in K["fotograflar"]}
    fotolar = {k: foto_yukle(o) for k, o in ogeler.items()}

    if a.sadece in (None, "foto"):
        for alt in ("akis_4x5", "hikaye_9x16", "carousel"):
            shutil.rmtree(CIKTI / alt, ignore_errors=True)
            (CIKTI / alt).mkdir(parents=True)
        for kod, im in fotolar.items():
            akis_4x5(im, ogeler[kod]).save(CIKTI / "akis_4x5" / f"{kod}.jpg", quality=93, subsampling=0)
            hikaye_9x16(im, ogeler[kod], K["hikaye_yazilari"][kod]).save(
                CIKTI / "hikaye_9x16" / f"{kod}.jpg", quality=93, subsampling=0)
        car = K["carousel"]
        for i, kod in enumerate(car["sira"], 1):
            akis_4x5(fotolar[kod], ogeler[kod]).save(CIKTI / "carousel" / f"kart{i:02d}-{kod}.jpg", quality=93, subsampling=0)
        kapanis_karti(u(1080), u(1350), "reklam", car["kapanis_baslik"], car["kapanis_alt"]).save(
            CIKTI / "carousel" / f"kart{len(car['sira']) + 1:02d}-kapanis.jpg", quality=93, subsampling=0)
        print(f"✔ {len(fotolar)} fotoğraf → akış 4:5 + hikâye 9:16 · carousel {len(car['sira']) + 1} kart")

    if a.sadece in (None, "video"):
        shutil.rmtree(CIKTI / "video", ignore_errors=True)
        (CIKTI / "video").mkdir(parents=True)
        V = K["videolar"]
        for ad, fn in (("R1", lambda: r1_uret(V["R1"], fotolar, ogeler, a.muzik)),
                       ("R2", lambda: r2_uret(V["R2"], fotolar, ogeler, a.muzik)),
                       ("organik_mario", lambda: organik_uret(V["organik_mario"]))):
            n = fn()
            print(f"✔ {V[ad]['cikti']}  ({n / FPS:.1f} sn){'  ← SADECE ORGANİK' if 'organik' in ad else ''}")
        for ad in (V["R1"]["cikti"], V["R2"]["cikti"]):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0.5", "-i", str(CIKTI / "video" / ad),
                            "-frames:v", "1", "-q:v", "2", str(CIKTI / "video" / ad.replace(".mp4", "-kapak.jpg"))],
                           check=True)
        if not a.muzik:
            print("ℹ Videolar sessiz kanal ile üretildi. Yayından önce: --muzik <Meta Ses Koleksiyonu parçası>")

    for w in dict.fromkeys(UYARILAR):
        print("⚠", w)


if __name__ == "__main__":
    main()
