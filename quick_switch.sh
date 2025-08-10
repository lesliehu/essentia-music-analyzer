#!/bin/bash
# Gyors modell váltó script

echo "🎭 GYORS MODELL VÁLTÓ"
echo "=================="

if [ ! -f "config.json" ]; then
    echo "❌ config.json nem található!"
    echo "🔧 Alapértelmezett konfiguráció létrehozása..."
    
    # Konfiguráció másolása a példa alapján
    if [ -f "config.json.example" ]; then
        cp config.json.example config.json
        echo "✅ Konfiguráció létrehozva config.json.example alapján"
    else
        # Egyszerű konfigurálható verzió futtatás a config létrehozásához
        echo "🚀 Konfiguráció generálása..."
        python3 -c "
import json
config = {
    'model_settings': {
        'active_model': 'discogs',
        'models': {
            'discogs': {
                'name': 'Discogs EffNet',
                'description': '400+ detailed genre categories',
                'model_file': 'models/classifier_model.pb',
                'labels_file': 'models/classifier_labels.json',
                'algorithm': 'TensorflowPredictEffnetDiscogs',
                'genre_count': 400,
                'performance': 'slow',
                'accuracy': 'excellent'
            },
            'musicnn': {
                'name': 'MusiCNN', 
                'description': '10 basic genres, fast processing',
                'model_file': 'essentia-models/musicnn/genre_dortmund_musicnn_msd.pb',
                'algorithm': 'TensorflowPredictMusiCNN',
                'genre_count': 10,
                'performance': 'fast',
                'accuracy': 'good',
                'genres': ['blues', 'country', 'disco', 'hiphop', 'jazz', 'reggae', 'rock', 'classical', 'electronic', 'folk']
            }
        }
    },
    'processing_settings': {
        'enable_bpm_analysis': True,
        'top_genres_count': 5,
        'confidence_threshold': 0.01
    },
    'output_settings': {
        'filename_prefix': 'music_analysis',
        'csv_encoding': 'utf-8-sig'
    }
}
with open('config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
print('✅ config.json létrehozva!')
"
    fi
    
    if [ ! -f "config.json" ]; then
        echo "❌ Konfiguráció létrehozása sikertelen!"
        exit 1
    fi
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