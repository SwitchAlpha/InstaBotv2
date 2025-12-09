#!/bin/bash
# ============================================================
# Instagram Bot API - Otomatik Kurulum (Mac/Linux)
# ============================================================

echo ""
echo "============================================================"
echo "  Instagram Bot API - Kurulum Başlatılıyor"
echo "============================================================"
echo ""

# Python kurulu mu kontrol et
if ! command -v python3 &> /dev/null; then
    echo "[HATA] Python3 bulunamadı!"
    echo ""
    echo "macOS için:"
    echo "  brew install python3"
    echo ""
    echo "Linux için:"
    echo "  sudo apt install python3 python3-pip"
    echo ""
    exit 1
fi

echo "[1/4] Python bulundu!"
python3 --version

# Virtual environment oluştur
echo ""
echo "[2/4] Virtual environment oluşturuluyor..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "[HATA] Virtual environment oluşturulamadı!"
    exit 1
fi

# Virtual environment'i aktifleştir
echo ""
echo "[3/4] Virtual environment aktif ediliyor..."
source venv/bin/activate

# Dependency'leri yükle
echo ""
echo "[4/4] Dependency'ler yükleniyor (bu birkaç dakika sürebilir)..."
echo ""
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[HATA] Dependency'ler yüklenemedi!"
    exit 1
fi

# Playwright browser'ı yükle
echo ""
echo "[BONUS] Playwright browser yükleniyor..."
playwright install chromium
if [ $? -ne 0 ]; then
    echo "[UYARI] Playwright browser yüklenemedi, manuel yüklemek gerekebilir."
fi

echo ""
echo "============================================================"
echo "  KURULUM TAMAMLANDI!"
echo "============================================================"
echo ""
echo "Kullanım:"
echo "  1. .env dosyasını düzenleyin (Instagram kullanıcı adı ve şifre)"
echo "  2. ./RUN.sh dosyasını çalıştırın"
echo ""
echo ".env örneği:"
echo "  IG_USERNAME=kullanici_adiniz"
echo "  IG_PASSWORD=sifreniz"
echo ""
echo "============================================================"
