#!/bin/bash
# Apple Silicon (M1/M2/M3) telepítő script

echo "🍎 ESSENTIA APPLE SILICON TELEPÍTŐ"
echo "=================================="

# Platform check
if [[ $(uname -s) != "Darwin" ]]; then
    echo "❌ Ez a script csak macOS-re készült!"
    exit 1
fi

if [[ $(uname -m) != "arm64" ]]; then
    echo "⚠️  Figyelem: Nem Apple Silicon platform ($(uname -m))"
    echo "ℹ️  A telepítés folytatódik, de optimalizációk nem lesznek aktívak"
fi

echo "🔍 Rendszer információ:"
echo "   OS: $(sw_vers -productName) $(sw_vers -productVersion)"
echo "   Chip: $(sysctl -n machdep.cpu.brand_string 2>/dev/null || echo 'Unknown')"
echo "   Architecture: $(uname -m)"
echo "   CPU cores: $(sysctl -n hw.ncpu)"
echo ""

# Homebrew ellenőrzés
if ! command -v brew &> /dev/null; then
    echo "⚠️  Homebrew nem található - telepítés ajánlott:"
    echo '   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    echo ""
else
    echo "✅ Homebrew telepítve: $(brew --version | head -1)"
fi

# Python ellenőrzés
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 nem található!"
    echo "💡 Telepítés: brew install python"
    exit 1
fi

echo "✅ Python: $(python3 --version)"
echo ""

# Virtual environment létrehozás
echo "🔧 Python virtual environment létrehozása..."
python3 -m venv essentia_apple_env
source essentia_apple_env/bin/activate

echo "✅ Virtual environment aktiválva"

# Pip frissítés
echo "📦 Pip frissítése..."
pip install --upgrade pip wheel setuptools

# Apple Silicon specific packages
echo "🍎 Apple Silicon optimalizált csomagok telepítése..."

# TensorFlow Apple Silicon verzió
pip install tensorflow-macos tensorflow-metal

# NumPy Apple Accelerate optimalizálással
pip install numpy

# Essentia és további függőségek
pip install -r requirements_apple.txt

echo ""
echo "🎵 Audio könyvtár létrehozása..."
mkdir -p audio_mp3
echo "📁 audio_mp3/ könyvtár létrehozva"

echo ""
echo "🧪 Telepítés tesztelése..."
python3 -c "
import platform
print(f'✅ Platform: {platform.system()} {platform.machine()}')

try:
    import numpy as np
    print(f'✅ NumPy: {np.__version__}')
    print(f'   BLAS: {np.show_config()}' if hasattr(np, 'show_config') else '   BLAS: N/A')
except Exception as e:
    print(f'❌ NumPy hiba: {e}')

try:
    import tensorflow as tf
    print(f'✅ TensorFlow: {tf.__version__}')
    gpus = tf.config.list_physical_devices('GPU')
    print(f'   Metal GPU: {len(gpus)} device' if gpus else '   Metal GPU: nem elérhető')
except Exception as e:
    print(f'❌ TensorFlow hiba: {e}')

try:
    import essentia
    print(f'✅ Essentia: {essentia.__version__}')
except Exception as e:
    print(f'❌ Essentia hiba: {e}')
"

echo ""
echo "🎉 APPLE SILICON TELEPÍTÉS BEFEJEZVE!"
echo ""
echo "💡 Használat:"
echo "   source essentia_apple_env/bin/activate"
echo "   ./run_apple.sh"
echo ""
echo "📝 Fájlok:"
echo "   • apple_essentia_silicon.py - Apple Silicon optimalizált verzió"
echo "   • run_apple.sh - Wrapper script"
echo "   • requirements_apple.txt - Apple dependencies"
echo "