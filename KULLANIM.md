# Instagram Bot API - Kullanım Kılavuzu

## 🚀 Hızlı Başlangıç (Teknik Bilgi Gerektirmez!)

### Windows Kullanıcıları

1. **Kurulum (Sadece İlk Seferde)**
   - `SETUP.bat` dosyasına çift tıklayın
   - Bekleyin (birkaç dakika sürer)
   - "KURULUM TAMAMLANDI!" yazısını görün

2. **Instagram Bilgilerini Girin**
   - `.env` dosyasını Not Defteri ile açın
   - Instagram kullanıcı adı ve şifrenizi yazın:
     ```
     IG_USERNAME=sizin_instagram_kullanici_adiniz
     IG_PASSWORD=sizin_sifreniz
     ```
   - Kaydet ve kapat

3. **Çalıştırın**
   - `RUN.bat` dosyasına çift tıklayın
   - Public URL otomatik kopyalanacak!

### Mac/Linux Kullanıcıları

1. **Kurulum (Sadece İlk Seferde)**
   - Terminal'i açın
   - Klasöre gidin: `cd ~/Desktop/InstaBotv2`
   - Çalıştırın: `./SETUP.sh`
   - Bekleyin

2. **Instagram Bilgilerini Girin**
   - `.env` dosyasını metin editörü ile açın
   - Instagram kullanıcı adı ve şifrenizi yazın
   - Kaydet ve kapat

3. **Çalıştırın**
   - Terminal'de: `./RUN.sh`
   - Public URL otomatik kopyalanacak!

## 📁 Dosya Yapısı

```
InstaBotv2/
├── SETUP.bat        ← Windows kurulum (çift tıkla)
├── SETUP.sh         ← Mac/Linux kurulum
├── RUN.bat          ← Windows çalıştır (çift tıkla)
├── RUN.sh           ← Mac/Linux çalıştır
├── .env             ← Instagram bilgileri (kendiniz oluşturun)
└── ... (diğer dosyalar)
```

## ⚙️ .env Dosyası Nasıl Oluşturulur?

**Windows:**
1. Sağ tık → Yeni → Metin Belgesi
2. Adını `.env` yapın (uzantısız!)
3. İçine şunu yazın:
   ```
   IG_USERNAME=kullanici_adi
   IG_PASSWORD=sifre
   ```
4. Kaydet

**Mac:**
1. TextEdit ile yeni dosya
2. Format → Düz Metin Yap
3. İçine yazın ve `.env` olarak kaydet

## 🌐 Public URL Nasıl Kullanılır?

Uygulama başladığında şöyle bir URL göreceksiniz:
```
✅ PUBLIC URL: https://abc-xyz-123.trycloudflare.com
📋 URL copied to clipboard!
```

Bu URL otomatik kopyalandı! Artık:
- Tarayıcıya yapıştırıp API'yi test edebilirsiniz
- Başka cihazlardan erişebilirsiniz
- Başkalarıyla paylaşabilirsiniz

## 🔧 Sorun Giderme

### "Python bulunamadı" hatası (Windows)
1. https://www.python.org/downloads/ adresinden Python indirin
2. Kurarken "Add Python to PATH" seçeneğini işaretleyin!
3. Bilgisayarı yeniden başlatın
4. `SETUP.bat` dosyasını tekrar çalıştırın

### "Python3 bulunamadı" hatası (Mac)
```bash
brew install python3
```

### Port 5001 kullanımda hatası
Başka bir Flask server çalışıyor olabilir:
- Windows: Task Manager'dan `python.exe` işlemlerini kapatın
- Mac: Terminal'de: `lsof -ti:5001 | xargs kill -9`

### Cloudflared indirme hatası
İnternet bağlantınızı kontrol edin ve tekrar deneyin.

## 📞 API Kullanımı

Public URL'iniz: `https://xyz.trycloudflare.com`

### 1. İlk Login
```bash
curl -X POST https://xyz.trycloudflare.com/login
```

### 2. Mesaj Gönder
```bash
curl -X POST https://xyz.trycloudflare.com/send \
  -H "Content-Type: application/json" \
  -d '{"username":"hedef_kullanici","message":"Merhaba!"}'
```

### 3. Sağlık Kontrolü
```bash
curl https://xyz.trycloudflare.com/health
```

## ✅ Hatırlatmalar

- ✅ `.env` dosyasını Git'e eklemeyin (şifreniz açıkta kalır!)
- ✅ Public URL her başlatmada değişir
- ✅ İlk çalıştırmada Cloudflared indirilir (~50MB)
- ✅ Instagram 2FA varsa tarayıcıda manuel girin
- ✅ Kapatmak için `Ctrl+C`

## 🎯 Özet

1. **İlk Kurulum**: `SETUP.bat` veya `./SETUP.sh`
2. **Instagram Bilgisi**: `.env` dosyası oluştur
3. **Çalıştır**: `RUN.bat` veya `./RUN.sh`
4. **Kullan**: Public URL otomatik kopyalanır!

Hepsi bu kadar! 🚀
