# Auto-Update Sistemi Kurulum Kılavuzu

## Nasıl Çalışır?

Uygulama her başlatıldığında:
1. GitHub'daki en son sürümü kontrol eder
2. Yeni sürüm varsa kullanıcıya sorar
3. Onay verilirse otomatik günceller
4. Uygulama yeniden başlatılır

## Kurulum Adımları

### 1. GitHub Repository Oluşturun

```bash
# GitHub'da yeni repo oluşturun: InstaBotv2
# Sonra local'de:
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/KULLANICI_ADINIZ/InstaBotv2.git
git push -u origin main
```

### 2. auto_update.py Dosyasını Düzenleyin

`auto_update.py` dosyasını açın ve GITHUB_REPO değişkenini güncelleyin:

```python
GITHUB_REPO = "KULLANICI_ADINIZ/InstaBotv2"  # Buraya kendi repo adresinizi yazın
```

### 3. İlk Sürümü Oluşturun

```bash
# VERSION dosyasına başlangıç versiyonu
echo "1.0.0" > VERSION

# Git'e ekle ve commit et
git add VERSION
git commit -m "v1.0.0"

# Tag oluştur
git tag v1.0.0
git push origin v1.0.0
```

## Yeni Sürüm Yayınlama

### Manuel Güncelleme (Kod Değişiklikleri)

1. **Kod değişikliklerini yapın**
```bash
# Değişiklikleri yap
git add .
git commit -m "Bug fixes and improvements"
```

2. **VERSION dosyasını güncelleyin**
```bash
# Yeni versiyon numarası
echo "1.0.1" > VERSION
git add VERSION
git commit -m "Bump version to 1.0.1"
```

3. **Tag oluşturup GitHub'a push edin**
```bash
git tag v1.0.1
git push origin main
git push origin v1.0.1
```

4. **GitHub Release oluşturun**
- GitHub'da repository sayfasına gidin
- "Releases" → "Create a new release"
- Tag: v1.0.1 seçin
- Release title: "v1.0.1"
- Description: Değişiklikleri açıklayın
- "Publish release"

### Otomatik Güncelleme (Clientlarda)

Kullanıcılar uygulamayı başlattığında:

```bash
python start.py
```

**Çıktı:**
```
============================================================
Checking for updates...
============================================================
Current version: 1.0.0
Latest version:  1.0.1

New version available: 1.0.1
Would you like to update now? (y/n): y

Updating via git pull...
Update successful!
Update complete! Please restart the application.
```

## Versiyon Numaralandırma

**Semantic Versioning kullanın: MAJOR.MINOR.PATCH**

- **MAJOR**: Uyumsuz API değişiklikleri (2.0.0)
- **MINOR**: Geriye uyumlu yeni özellikler (1.1.0)
- **PATCH**: Geriye uyumlu bug fix'ler (1.0.1)

**Örnekler:**
- `1.0.0` → İlk sürüm
- `1.0.1` → Bug fix
- `1.1.0` → Yeni özellik eklendi
- `2.0.0` → Büyük değişiklik (breaking changes)

## Client Kurulumu için .git Klasörü

Kullanıcıların otomatik güncelleme alabilmesi için:

```bash
# Kullanıcılar repo'yu clone etmeli:
git clone https://github.com/KULLANICI_ADINIZ/InstaBotv2.git
cd InstaBotv2

# Kurulum
./SETUP.sh  # veya SETUP.bat

# Çalıştır
./RUN.sh    # veya RUN.bat
```

## Sorun Giderme

### "Could not check for updates"
- İnternet bağlantısını kontrol edin
- GitHub repo adresinin doğru olduğundan emin olun

### "Git pull failed"
- `.git` klasörü mevcut olmalı
- Kullanıcı değişiklikleri commit edilmeli veya stash edilmeli

### Manuel Güncelleme
Otomatik güncelleme çalışmazsa:

```bash
cd InstaBotv2
git pull origin main
```

## Güncelleme Akışı Özeti

**Developer (Siz):**
1. Kod değişiklikleri yap
2. VERSION dosyasını güncelle
3. Git tag oluştur
4. GitHub'a push et
5. GitHub Release oluştur

**Users (Clientlar):**
1. `python start.py` çalıştır
2. Güncelleme mesajı gelirse "y" tuşla
3. Otomatik indirilir ve güncellenir
4. Uygulamayı yeniden başlat

---

**Tüm clientlar GitHub'a her push yaptığınızda otomatik güncellenecek!** 🚀
