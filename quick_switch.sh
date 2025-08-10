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
echo "🎯 Csak a Discogs EffNet modell elérhető"
echo "  • 400+ részletes műfaj kategória"
echo "  • Pontos és megbízható eredmények"
echo "  • Professzionális minőség"
echo ""

echo "✅ Discogs EffNet modell már aktív"
python3 config_editor.py set-model discogs

echo ""
echo "✅ Modell váltás kész!"
echo "🚀 Futtatáshoz használd: ./run_silent.sh"