#!/bin/bash
# Linux x86 környezet beállítása az Essentia zene elemzőhöz

echo "🎼 ESSENTIA ZENE ELEMZŐ - Linux x86 telepítő"
echo "================================================="

# Python verzió ellenőrzés
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
echo "Python verzió: $python_version"

if [[ $(echo "$python_version < 3.8" | bc -l) -eq 1 ]]; then
    echo "❌ Hiba: Python 3.8 vagy újabb szükséges!"
    exit 1
fi

# Virtuális környezet létrehozása
echo "📦 Virtuális környezet létrehozása..."
python3 -m venv essentia_env
source essentia_env/bin/activate

# Csomagok telepítése
echo "📥 Függőségek telepítése..."
pip install --upgrade pip
pip install -r requirements.txt

# Könyvtárak létrehozása
echo "📁 Könyvtárak létrehozása..."
mkdir -p models
mkdir -p audio_mp3
mkdir -p results

# Jogosultságok beállítása
chmod +x linux_essentia.py

echo ""
echo "✅ Telepítés befejezve!"
echo ""
echo "🚀 HASZNÁLAT:"
echo "   1. Aktiváld a virtuális környezetet:"
echo "      source essentia_env/bin/activate"
echo ""
echo "   2. Helyezz audio fájlokat az 'audio_mp3' könyvtárba"
echo ""
echo "   3. Futtasd az elemzőt:"
echo "      python3 linux_essentia.py"
echo ""
echo "   4. Az eredményeket az 'eredmenyek_*.csv' fájlokban találod"
echo ""
echo "================================================="