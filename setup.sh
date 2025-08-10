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

# Ellenőrizzük a requirements.txt létezését
if [ ! -f requirements.txt ]; then
    echo "❌ requirements.txt nem található!"
    exit 1
fi

pip install -r requirements.txt

# Ellenőrizzük az Essentia telepítését
echo "🔍 Essentia telepítés ellenőrzése..."
if ! python3 -c "import essentia" 2>/dev/null; then
    echo "⚠️ Essentia telepítés sikertelen, újrapróbálás..."
    pip install essentia-tensorflow==2.1b6.dev1389
fi

# Könyvtárak létrehozása
echo "📁 Könyvtárak létrehozása..."
mkdir -p models
mkdir -p audio_mp3
mkdir -p results

# Jogosultságok beállítása
chmod +x linux_essentia_optimized.py

echo ""
echo "✅ Telepítés befejezve!"
echo ""
echo "🚀 HASZNÁLAT:"
echo "   1. Aktiváld a virtuális környezetet:"
echo "      source essentia_env/bin/activate"
echo ""
echo "   2. Git LFS modellek letöltése (ha szükséges):"
echo "      git lfs pull"
echo ""
echo "   3. Helyezz audio fájlokat az 'audio_mp3' könyvtárba"
echo ""
echo "   4. Futtasd az elemzőt:"
echo "      python3 linux_essentia_optimized.py"
echo ""
echo "   5. Az eredményeket a 'tensorflow_eredmenyek_*.csv' fájlokban találod"
echo ""
echo "================================================="