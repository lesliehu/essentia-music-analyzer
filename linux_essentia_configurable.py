#!/usr/bin/env python3
"""
Essentia zene műfaj elemző - Konfigurálható több-modell verzió
Választható modellek: Discogs EffNet (400+ műfaj) vagy MusiCNN (10 műfaj)
"""
import os
import sys
import time
import json
import logging
from datetime import datetime

# TensorFlow és Essentia logging csendesítés
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['ESSENTIA_LOGGING_LEVEL'] = 'ERROR'
logging.getLogger('tensorflow').setLevel(logging.ERROR)
logging.getLogger('essentia').setLevel(logging.ERROR)

import numpy as np
import pandas as pd
import urllib.request

# Essentia import ellenőrzéssel
try:
    import essentia
    import essentia.standard as es
    print("✅ Essentia betöltve (verzió: {})".format(essentia.__version__))
except ImportError:
    print("❌ Hiba: Essentia nincs telepítve!")
    print("Telepítés: pip install essentia-tensorflow")
    sys.exit(1)


class ConfigurableGenreClassifier:
    """
    Konfigurálható műfaj osztályozó több modell támogatással
    """
    def __init__(self, config_path="config.json"):
        self.config = self.load_config(config_path)
        self.model_loaded = False
        self.predictor = None
        self.labels = None
        self.current_model_info = None
        
    def load_config(self, config_path):
        """Konfiguráció betöltése"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"✅ Konfiguráció betöltve: {config_path}")
            return config
        except Exception as e:
            print(f"❌ Konfiguráció betöltési hiba: {e}")
            print("🔧 Alapértelmezett konfiguráció használata...")
            return self.get_default_config()
    
    def get_default_config(self):
        """Alapértelmezett konfiguráció"""
        return {
            "model_settings": {
                "active_model": "discogs",
                "models": {
                    "discogs": {
                        "name": "Discogs EffNet",
                        "model_file": "models/classifier_model.pb",
                        "labels_file": "models/classifier_labels.json",
                        "algorithm": "TensorflowPredictEffnetDiscogs",
                        "sample_rate": 16000
                    }
                }
            },
            "processing_settings": {
                "enable_bmp_analysis": True,
                "top_genres_count": 5
            }
        }
    
    def show_available_models(self):
        """Elérhető modellek megjelenítése"""
        print("\n🎭 ELÉRHETŐ MODELLEK:")
        print("=" * 50)
        
        models = self.config["model_settings"]["models"]
        active = self.config["model_settings"]["active_model"]
        
        for model_key, model_info in models.items():
            status = "🟢 AKTÍV" if model_key == active else "⚪ Elérhető"
            print(f"\n{status} - {model_key.upper()}")
            print(f"  📛 Név: {model_info['name']}")
            print(f"  📝 Leírás: {model_info['description']}")
            print(f"  🎯 Műfajok: {model_info['genre_count']}")
            print(f"  ⚡ Sebesség: {model_info['performance']}")
            print(f"  🎯 Pontosság: {model_info['accuracy']}")
            
            # Fájl ellenőrzés
            model_file = model_info['model_file']
            if os.path.exists(model_file):
                size_mb = os.path.getsize(model_file) / (1024*1024)
                print(f"  💾 Fájl: {model_file} ({size_mb:.1f} MB) ✅")
            else:
                print(f"  💾 Fájl: {model_file} ❌ HIÁNYZIK")
    
    def download_model_files(self, model_key=None):
        """Modell fájlok letöltése"""
        if model_key is None:
            model_key = self.config["model_settings"]["active_model"]
        
        model_info = self.config["model_settings"]["models"][model_key]
        
        print(f"\n📥 {model_info['name']} fájlok ellenőrzése...")
        
        downloads = []
        if model_info.get('download_url'):
            downloads.append((model_info['model_file'], model_info['download_url']))
        if model_info.get('labels_url'):
            downloads.append((model_info['labels_file'], model_info['labels_url']))
        
        if not downloads:
            print("✅ Helyi modell, nincs letöltés szükséges")
            return True
        
        for file_path, url in downloads:
            # Könyvtár létrehozása
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            if not os.path.exists(file_path):
                print(f"📥 Letöltés: {os.path.basename(file_path)}...")
                try:
                    urllib.request.urlretrieve(url, file_path)
                    size_mb = os.path.getsize(file_path) / (1024*1024)
                    print(f"✅ {os.path.basename(file_path)} letöltve ({size_mb:.1f} MB)")
                except Exception as e:
                    print(f"❌ Letöltési hiba: {e}")
                    return False
            else:
                size_mb = os.path.getsize(file_path) / (1024*1024)
                print(f"✅ {os.path.basename(file_path)} létezik ({size_mb:.1f} MB)")
        
        return True
    
    def load_model(self, model_key=None):
        """Modell betöltése"""
        if model_key is None:
            model_key = self.config["model_settings"]["active_model"]
        
        if model_key not in self.config["model_settings"]["models"]:
            print(f"❌ Ismeretlen modell: {model_key}")
            return False
        
        model_info = self.config["model_settings"]["models"][model_key]
        self.current_model_info = model_info
        
        model_path = model_info['model_file']
        if not os.path.exists(model_path):
            print(f"❌ Modell fájl nem található: {model_path}")
            return False
        
        try:
            print(f"🤖 {model_info['name']} modell betöltése...")
            start_time = time.time()
            
            # Algoritmus típus szerint betöltés
            algorithm = model_info['algorithm']
            
            if algorithm == "TensorflowPredictEffnetDiscogs":
                self.predictor = es.TensorflowPredictEffnetDiscogs(graphFilename=model_path)
                self.labels = self.load_discogs_labels(model_info.get('labels_file'))
                
            elif algorithm == "TensorflowPredictMusiCNN":
                self.predictor = es.TensorflowPredictMusiCNN(graphFilename=model_path)
                self.labels = model_info.get('genres', ['unknown'])
                
            else:
                # Általános TensorFlow predictor
                self.predictor = es.TensorflowPredict2D(graphFilename=model_path)
                self.labels = model_info.get('genres', ['unknown'])
            
            load_time = time.time() - start_time
            print(f"✅ {model_info['name']} betöltve ({load_time:.1f}s)")
            print(f"   Műfajok száma: {len(self.labels)}")
            print(f"   Sebesség: {model_info.get('performance', 'unknown')}")
            print(f"   Pontosság: {model_info.get('accuracy', 'unknown')}")
            
            self.model_loaded = True
            return True
            
        except Exception as e:
            print(f"❌ Modell betöltési hiba: {e}")
            return False
    
    def load_discogs_labels(self, labels_file):
        """Discogs címkék betöltése"""
        if not labels_file or not os.path.exists(labels_file):
            print("⚠️ Discogs labels fájl hiányzik, alapértelmezett használata")
            return ["Electronic", "Rock", "Pop", "Jazz", "Classical"]
        
        try:
            with open(labels_file, "r", encoding='utf-8') as f:
                labels_info = json.load(f)
            return labels_info["classes"]
        except Exception as e:
            print(f"⚠️ Labels betöltési hiba: {e}")
            return ["Electronic", "Rock", "Pop", "Jazz", "Classical"]
    
    def analyze_audio(self, file_path):
        """Audio elemzés a konfigurált modellel"""
        if not self.model_loaded:
            return {'success': False, 'error': 'Nincs betöltött modell'}
        
        config = self.config["processing_settings"]
        
        try:
            print(f"  🎵 Elemzés: {os.path.basename(file_path)}")
            
            # BPM számítás (ha engedélyezve)
            bpm = 0
            if config.get("enable_bpm_analysis", True):
                print("    📊 BPM számítás...")
                audio_44k = es.MonoLoader(filename=file_path, sampleRate=44100)()
                ticks, confidence = es.BeatTrackerMultiFeature()(audio_44k)
                bpm = 60.0 / np.median(np.diff(ticks)) if len(ticks) > 1 else 0
            
            # Műfaj predikció
            print(f"    🤖 Műfaj predikció ({self.current_model_info['name']})...")
            sample_rate = self.current_model_info.get('sample_rate', 16000)
            audio = es.MonoLoader(filename=file_path, sampleRate=sample_rate)()
            
            # Predikció futtatása
            predictions = self.predictor(audio)
            
            # Eredmények feldolgozása
            top_count = config.get("top_genres_count", 5)
            confidence_threshold = config.get("confidence_threshold", 0.01)
            
            if len(predictions) > 0 and len(predictions[0]) > 0:
                # Predictions és labels párosítása
                results = list(zip(self.labels[:len(predictions[0])], predictions[0]))
                
                # Szűrés és rendezés
                filtered_results = [(genre, conf) for genre, conf in results 
                                  if conf >= confidence_threshold]
                top_genres = sorted(filtered_results, key=lambda x: x[1], reverse=True)[:top_count]
            else:
                top_genres = [("Unknown", 0.0)]
            
            return {
                'success': True,
                'bpm': round(bpm, 1),
                'genres': top_genres,
                'model_used': self.current_model_info['name'],
                'model_key': self.config["model_settings"]["active_model"],
                'audio_length': len(audio) / sample_rate,
                'genre_count': len(self.labels)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


def check_audio_directory():
    """Audio könyvtár ellenőrzése"""
    audio_dir = "audio_mp3"
    
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir, exist_ok=True)
        print(f"📁 '{audio_dir}' könyvtár létrehozva")
        return [], audio_dir
    
    # Támogatott formátumok a config-ból vagy alapértelmezett
    supported_formats = ['.mp3', '.wav', '.flac', '.ogg', '.m4a']
    
    audio_files = []
    for file in os.listdir(audio_dir):
        if any(file.lower().endswith(fmt) for fmt in supported_formats):
            audio_files.append(file)
    
    print(f"📁 Audio fájlok ({len(audio_files)}): {audio_dir}/")
    for file in audio_files[:3]:
        size = os.path.getsize(os.path.join(audio_dir, file)) / (1024*1024)
        print(f"  • {file} ({size:.1f} MB)")
    if len(audio_files) > 3:
        print(f"  ... és még {len(audio_files) - 3} fájl")
    
    return audio_files, audio_dir


def process_configurable_batch(classifier, audio_files, audio_dir):
    """Konfigurálható batch feldolgozás"""
    config = classifier.config
    model_name = classifier.current_model_info['name']
    
    print(f"\n🚀 KONFIGURÁLHATÓ BATCH FELDOLGOZÁS")
    print(f"🤖 Modell: {model_name}")
    print(f"📂 Fájlok: {len(audio_files)}")
    print("="*60)
    
    results = []
    errors = []
    start_time = datetime.now()
    total_audio_time = 0
    
    for idx, filename in enumerate(audio_files, 1):
        file_path = os.path.join(audio_dir, filename)
        print(f"\n[{idx}/{len(audio_files)}] {filename}")
        print("-" * 50)
        
        analysis_start = time.time()
        result = classifier.analyze_audio(file_path)
        analysis_time = time.time() - analysis_start
        
        if not result['success']:
            print(f"    ❌ Hiba: {result['error']}")
            errors.append({'fajl': filename, 'hiba': result['error']})
            continue
        
        # Eredmények megjelenítése
        print(f"    ✅ BPM: {result['bpm']}")
        print(f"    🤖 Modell: {result['model_used']}")
        print(f"    📊 Műfajok száma: {result['genre_count']}")
        print(f"    ⏱️  Idő: {analysis_time:.1f}s")
        print("    🏆 Top műfajok:")
        
        for i, (genre, conf) in enumerate(result['genres'], 1):
            if isinstance(genre, str) and '---' in genre:
                genre_clean = genre.replace('---', ' / ')
            else:
                genre_clean = str(genre)
            print(f"      {i}. {genre_clean}: {conf:.1%}")
        
        # CSV adatok összeállítása
        row = {
            'fajl': filename,
            'BPM': result['bpm'],
            'modell': result['model_key'],
            'modell_nev': result['model_used'],
            'mufaj_szam': result['genre_count'],
            'feldolgozasi_ido_sec': round(analysis_time, 1),
            'audio_hossz_sec': round(result['audio_length'], 1),
            'feldolgozas_ideje': datetime.now().strftime(
                config["output_settings"].get("timestamp_format", "%Y-%m-%d %H:%M:%S")
            )
        }
        
        # Top műfajok hozzáadása
        top_count = config["processing_settings"].get("top_genres_count", 5)
        for i, (genre, conf) in enumerate(result['genres'][:top_count], 1):
            if isinstance(genre, str) and '---' in genre:
                genre_clean = genre.replace('---', ' / ')
            else:
                genre_clean = str(genre)
            row[f'Genre_{i}'] = genre_clean
            row[f'Conf_{i}'] = round(float(conf), 4)
        
        results.append(row)
        total_audio_time += result['audio_length']
        print("    ✅ Sikeres feldolgozás")
    
    # Feldolgozási statisztikák
    processing_time = (datetime.now() - start_time).total_seconds()
    
    print(f"\n{'='*60}")
    print("📊 KONFIGURÁLHATÓ BATCH FELDOLGOZÁS BEFEJEZVE")
    print(f"{'='*60}")
    print(f"🤖 Használt modell: {model_name}")
    print(f"⏱️  Teljes feldolgozási idő: {processing_time:.1f}s")
    print(f"🎼 Összes audio idő: {total_audio_time:.1f}s")
    if processing_time > 0:
        print(f"📊 Sebesség: {total_audio_time/processing_time:.1f}x realtime")
    print(f"✅ Sikeres fájlok: {len(results)}")
    print(f"❌ Hibás fájlok: {len(errors)}")
    
    return results, errors, processing_time


def save_configurable_results(results, errors, classifier):
    """Konfigurálható eredmények mentése"""
    config = classifier.config["output_settings"]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    saved_files = []
    
    # Eredmények mentése
    if results:
        prefix = config.get("filename_prefix", "music_analysis")
        model_key = classifier.config["model_settings"]["active_model"]
        filename = f"{prefix}_{model_key}_{timestamp}.csv"
        
        df = pd.DataFrame(results)
        encoding = config.get("csv_encoding", "utf-8-sig")
        df.to_csv(filename, index=False, encoding=encoding)
        
        print(f"\n💾 Eredmények mentve: {filename}")
        saved_files.append(filename)
        
        # Statisztikák
        print(f"\n📈 STATISZTIKÁK:")
        print(f"  • Modell: {results[0]['modell_nev'] if results else 'N/A'}")
        print(f"  • Fájlok: {len(df)}")
        print(f"  • Átlag BPM: {df['BPM'].mean():.1f}")
        print(f"  • Átlag feldolgozási idő: {df['feldolgozasi_ido_sec'].mean():.1f}s")
        
        if 'Genre_1' in df.columns:
            top_genre = df['Genre_1'].mode().values[0] if not df.empty else 'N/A'
            print(f"  • Leggyakoribb műfaj: {top_genre}")
        
        if 'Conf_1' in df.columns:
            print(f"  • Átlagos konfidencia: {df['Conf_1'].mean():.1%}")
    
    # Hibák mentése
    if errors:
        error_filename = f"hibak_{timestamp}.csv"
        df_errors = pd.DataFrame(errors)
        df_errors.to_csv(error_filename, index=False, encoding='utf-8-sig')
        print(f"\n⚠️ Hibák mentve: {error_filename}")
        saved_files.append(error_filename)
    
    return saved_files


def main():
    """Fő függvény - konfigurálható verzió"""
    print("🎭 ESSENTIA KONFIGURÁLHATÓ MŰFAJ ELEMZŐ")
    print("="*60)
    print("🔧 Több modell támogatással és testreszabható beállításokkal")
    print("="*60)
    
    try:
        # Osztályozó inicializálása
        classifier = ConfigurableGenreClassifier()
        
        # Elérhető modellek megjelenítése
        classifier.show_available_models()
        
        # Aktív modell fájlok letöltése/ellenőrzése
        print(f"\n1️⃣ Aktív modell fájlok ellenőrzése...")
        if not classifier.download_model_files():
            print("❌ Modell fájlok problémája!")
            return 1
        
        # Modell betöltése
        print(f"\n2️⃣ Modell betöltése...")
        if not classifier.load_model():
            print("❌ Modell betöltés sikertelen!")
            return 1
        
        # Audio fájlok keresése
        print(f"\n3️⃣ Audio fájlok keresése...")
        audio_files, audio_dir = check_audio_directory()
        
        if not audio_files:
            print(f"\n⚠️ Nincs feldolgozható fájl!")
            print(f"📁 Helyezz audio fájlokat a '{audio_dir}' könyvtárba")
            return 0
        
        # Batch feldolgozás
        print(f"\n4️⃣ Konfigurálható batch feldolgozás...")
        results, errors, proc_time = process_configurable_batch(
            classifier, audio_files, audio_dir
        )
        
        # Eredmények mentése
        print(f"\n5️⃣ Eredmények mentése...")
        saved_files = save_configurable_results(results, errors, classifier)
        
        print(f"\n🎉 FELDOLGOZÁS BEFEJEZVE!")
        print(f"💾 Mentett fájlok: {', '.join(saved_files)}")
        print(f"⏱️  Teljes idő: {proc_time:.1f} másodperc")
        print(f"\n💡 A modellt a config.json fájlban változtathatod meg!")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Feldolgozás megszakítva")
        return 1
    except Exception as e:
        print(f"\n❌ Váratlan hiba: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())