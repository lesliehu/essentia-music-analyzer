#!/bin/bash
# Gyors modell váltó script

echo "🎭 GYORS MODELL VÁLTÓ"
echo "=================="

if [ ! -f "config.json" ]; then
    echo "❌ config.json nem található!"
    echo "💡 Futtasd először: python3 linux_essentia_configurable.py"
    exit 1
fi

# Jelenlegi modell megjelenítése
echo "📋 Jelenlegi konfiguráció:"
python3 config_editor.py show | grep -A5 "🤖 Aktív modell"

echo ""
echo "🔄 Elérhető modellek:"
echo "  1. discogs  (400+ műfaj, lassú, precíz)"
echo "  2. musicnn  (10 műfaj, gyors, jó)"
echo ""

read -p "Válassz modellt (1/2): " choice

case $choice in
    1)
        echo "🔄 Váltás Discogs EffNet modellre..."
        python3 config_editor.py set-model discogs
        ;;
    2)
        echo "🔄 Váltás MusiCNN modellre..."
        python3 config_editor.py set-model musicnn
        ;;
    *)
        echo "❌ Érvénytelen választás!"
        exit 1
        ;;
esac

echo ""
echo "✅ Modell váltás kész!"
echo "🚀 Futtatáshoz használd: ./run_silent.sh"