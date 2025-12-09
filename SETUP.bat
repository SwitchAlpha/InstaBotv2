@echo off
REM ============================================================
REM Instagram Bot API - Otomatik Kurulum (Windows)
REM ============================================================

echo.
echo ============================================================
echo   Instagram Bot API - Kurulum Baslatiyor
echo ============================================================
echo.

REM Python kurulu mu kontrol et
python --version >nul 2>&1
if errorlevel 1 (
    echo [HATA] Python bulunamadi!
    echo.
    echo Lutfen once Python yukleyin:
    echo https://www.python.org/downloads/
    echo.
    echo Kurulum sirasinda "Add Python to PATH" secenegini isaretleyin!
    pause
    exit /b 1
)

echo [1/4] Python bulundu!
python --version

REM Virtual environment olustur
echo.
echo [2/4] Virtual environment olusturuluyor...
python -m venv venv
if errorlevel 1 (
    echo [HATA] Virtual environment olusturulamadi!
    pause
    exit /b 1
)

REM Virtual environment'i aktiflet
echo.
echo [3/4] Virtual environment aktif ediliyor...
call venv\Scripts\activate.bat

REM Dependency'leri yukle
echo.
echo [4/4] Dependency'ler yukleniyor (bu birkaç dakika sürebilir)...
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo [HATA] Dependency'ler yuklenemedi!
    pause
    exit /b 1
)

REM Playwright browser'i yukle
echo.
echo [BONUS] Playwright browser yukleniyor...
playwright install chromium
if errorlevel 1 (
    echo [UYARI] Playwright browser yuklenemedi, manuel yuklemek gerekebilir.
)

echo.
echo ============================================================
echo   KURULUM TAMAMLANDI!
echo ============================================================
echo.
echo Kullanim:
echo   1. .env dosyasini duzenleyin (Instagram kullanici adi ve sifre)
echo   2. RUN.bat dosyasini cift tiklayin
echo.
echo .env ornegi:
echo   IG_USERNAME=kullanici_adiniz
echo   IG_PASSWORD=sifreniz
echo.
echo ============================================================
pause
