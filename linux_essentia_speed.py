#!/usr/bin/env python3
"""
Essentia zene műfaj elemző - SEBESSÉG OPTIMALIZÁLT verzió
Gyorsított feldolgozás: egyetlen audio betöltés + Essentia resample
"""
import os
import sys
import time
import json
import logging
from datetime import datetime

# MAXIMÁLIS TensorFlow és Essentia csendesítés
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['ESSENTIA_LOGGING_LEVEL'] = 'ERROR'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['KMP_AFFINITY'] = 'noverbose'
os.environ['TF_AUTOTUNE_THRESHOLD'] = '1'
os.environ['GLOG_minloglevel'] = '3'
os.environ['TF_SUPPRESS_LOGS'] = '1'

# Összes warning és info kikapcsolása
import warnings
warnings.filterwarnings('ignore', category=Warning)
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

import logging
logging.getLogger('tensorflow').setLevel(logging.CRITICAL)
logging.getLogger('essentia').setLevel(logging.CRITICAL)
logging.getLogger('absl').setLevel(logging.CRITICAL)
logging.getLogger().setLevel(logging.CRITICAL)

# Root logger teljes kikapcsolás
logging.disable(logging.WARNING)

# Stderr csendesítés TensorFlow-hoz
import sys
from contextlib import redirect_stderr
import io

import numpy as np
import pandas as pd
import urllib.request

# Essentia import teljes csendesítéssel
try:
    # TensorFlow import előtt stderr elnyomás
    stderr_buffer = io.StringIO()
    with redirect_stderr(stderr_buffer):
        import essentia
        import essentia.standard as es
        
        # Maximális Essentia csendesítés
        essentia.log.silent()
        essentia.log.setLevel(essentia.EAlgorithmLogLevel.SILENT)
    
    print("✅ Essentia betöltve (verzió: {})".format(essentia.__version__))
except ImportError:
    print("❌ Hiba: Essentia nincs telepítve!")
    print("Telepítés: pip install essentia-tensorflow")
    sys.exit(1)
except Exception:
    # Ha a csendesítés nem működik, folytatjuk
    print("✅ Essentia betöltve")


class MusicGenreClassifier:
    """
    Optimalizált műfaj osztályozó TensorFlow modellel
    """
    def __init__(self):
        self.model_loaded = False
        self.predictor = None
        self.labels = None
        
    def download_models(self):
        """Modell fájlok letöltése"""
        files_to_check = {
            "classifier_model.pb": "https://essentia.upf.edu/models/music-style-classification/discogs-effnet/discogs-effnet-bs64-1.pb",
            "classifier_labels.json": "https://essentia.upf.edu/models/music-style-classification/discogs-effnet/discogs-effnet-bs64-1.json"
        }
        
        models_dir = "models"
        if not os.path.exists(models_dir):
            os.makedirs(models_dir, exist_ok=True)
        
        for filename, url in files_to_check.items():
            file_path = os.path.join(models_dir, filename)
            if not os.path.exists(file_path):
                print(f"📥 Letöltés: {filename}...")
                try:
                    urllib.request.urlretrieve(url, file_path)
                    size_mb = os.path.getsize(file_path) / (1024*1024)
                    print(f"✅ {filename} letöltve ({size_mb:.1f} MB)")
                except Exception as e:
                    print(f"❌ Letöltési hiba ({filename}): {e}")
                    return False
            else:
                size_mb = os.path.getsize(file_path) / (1024*1024)
                print(f"✅ {filename} létezik ({size_mb:.1f} MB)")
        
        return True
    
    def load_model(self):
        """Modell és címkék betöltése (egyszer)"""
        if self.model_loaded:
            return True
            
        model_path = os.path.join("models", "classifier_model.pb")
        labels_path = os.path.join("models", "classifier_labels.json")
        
        if not os.path.exists(model_path) or not os.path.exists(labels_path):
            print("❌ Modell fájlok hiányoznak!")
            return False
        
        try:
            print("🤖 TensorFlow modell betöltése...")
            start_time = time.time()
            
            # Modell betöltése csendben
            stderr_buffer = io.StringIO()
            with redirect_stderr(stderr_buffer):
                self.predictor = es.TensorflowPredictEffnetDiscogs(graphFilename=model_path)
            
            # Címkék betöltése
            with open(labels_path, "r") as f:
                labels_info = json.load(f)
            self.labels = labels_info["classes"]
            
            load_time = time.time() - start_time
            print(f"✅ Modell betöltve ({load_time:.1f}s, {len(self.labels)} műfaj)")
            self.model_loaded = True
            return True
            
        except Exception as e:
            print(f"❌ Modell betöltési hiba: {e}")
            return False
    
    def analyze_audio(self, file_path, skip_bpm=False):
        """
        Optimalizált audio elemzés - opcionális BPM számítás
        """
        try:
            print(f"  🎵 Feldolgozás: {os.path.basename(file_path)}")
            
            if skip_bpm:
                # Csak műfaj elemzés - 30-50% gyorsabb
                print("    🤖 Műfaj predikció (BPM kihagyva)...")
                audio_16k = es.MonoLoader(filename=file_path, sampleRate=16000)()
                stderr_buffer = io.StringIO()
                with redirect_stderr(stderr_buffer):
                    activations = self.predictor(audio_16k)
                
                # Top 5 műfaj
                genre_results = sorted(
                    zip(self.labels, activations[0]), 
                    key=lambda x: x[1], 
                    reverse=True
                )[:5]
                
                return {
                    'success': True,
                    'bpm': 0,  # Nem számolva
                    'genres': genre_results,
                    'audio_length': len(audio_16k) / 16000.0
                }
            else:
                # Teljes elemzés - optimalizált resample-lel
                print("    🎵 Audio betöltés (44kHz)...")
                audio_44k = es.MonoLoader(filename=file_path, sampleRate=44100)()
                
                print("    📊 BPM számítás...")
                ticks, confidence = es.BeatTrackerMultiFeature()(audio_44k)
                bpm = 60.0 / np.median(np.diff(ticks)) if len(ticks) > 1 else 0
                
                print("    🔄 Essentia resample...")
                # Essentia resample (optimalizált)
                resampler = es.Resample(inputSampleRate=44100, outputSampleRate=16000)
                audio_16k = resampler(audio_44k)
                
                print("    🤖 Műfaj predikció...")
                stderr_buffer = io.StringIO()
                with redirect_stderr(stderr_buffer):
                    activations = self.predictor(audio_16k)
                
                # Top 5 műfaj (vectorizált rendezés - gyorsabb)
                probabilities = activations[0]
                top_indices = np.argpartition(probabilities, -5)[-5:]
                top_indices = top_indices[np.argsort(-probabilities[top_indices])]
                genre_results = [(self.labels[i], probabilities[i]) for i in top_indices]
                
                return {
                    'success': True,
                    'bpm': round(bpm, 1),
                    'genres': genre_results,
                    'audio_length': len(audio_44k) / 44100.0
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
    
    supported_formats = ['.mp3', '.wav', '.flac', '.ogg', '.m4a']
    audio_files = []
    
    for file in os.listdir(audio_dir):
        if any(file.lower().endswith(fmt) for fmt in supported_formats):
            audio_files.append(file)
    
    if audio_files:
        print(f"📁 Talált fájlok ({len(audio_files)}):")
        for i, file in enumerate(audio_files[:5], 1):
            size_mb = os.path.getsize(os.path.join(audio_dir, file)) / (1024*1024)
            print(f"  {i}. {file} ({size_mb:.1f} MB)")
        if len(audio_files) > 5:
            print(f"  ... és még {len(audio_files) - 5} fájl")
    else:
        print(f"📁 '{audio_dir}' könyvtár üres")
    
    return audio_files, audio_dir


def process_batch_tensorflow(classifier, audio_files, audio_dir):
    """
    Batch feldolgozás TensorFlow modellel
    """
    print(f"\n🚀 TENSORFLOW BATCH FELDOLGOZÁS")
    print(f"📂 Fájlok száma: {len(audio_files)}")
    print("="*60)
    
    results = []
    errors = []
    start_time = datetime.now()
    total_audio_time = 0
    
    for idx, filename in enumerate(audio_files, 1):
        file_path = os.path.join(audio_dir, filename)
        
        print(f"\n[{idx}/{len(audio_files)}] {filename}")
        print("-" * 50)
        
        # Elemzés
        analysis_start = time.time()
        result = classifier.analyze_audio(file_path)
        analysis_time = time.time() - analysis_start
        
        if not result['success']:
            print(f"    ❌ Hiba: {result['error']}")
            errors.append({'fajl': filename, 'hiba': result['error']})
            continue
        
        # Eredmények megjelenítése
        print(f"    ✅ BPM: {result['bpm']}")
        print(f"    ⏱️  Feldolgozási idő: {analysis_time:.1f}s")
        print(f"    🎼 Audio hossz: {result['audio_length']:.1f}s")
        print("    🏆 Top műfajok:")
        
        for i, (genre, conf) in enumerate(result['genres'], 1):
            clean_genre = genre.replace('---', ' / ')
            print(f"      {i}. {clean_genre}: {conf:.1%}")
        
        # CSV adatok összeállítása
        row = {
            'fajl': filename,
            'BPM': result['bpm'],
            'audio_hossz_sec': round(result['audio_length'], 1),
            'feldolgozasi_ido_sec': round(analysis_time, 1),
            'feldolgozas_ideje': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Top 5 műfaj hozzáadása
        for i, (genre, conf) in enumerate(result['genres'], 1):
            row[f'Genre_{i}'] = genre.replace('---', ' / ')
            row[f'Conf_{i}'] = round(float(conf), 4)
        
        results.append(row)
        total_audio_time += result['audio_length']
        
        print("    ✅ Sikeres feldolgozás")
    
    # Összesített statisztikák
    processing_time = (datetime.now() - start_time).total_seconds()
    
    print(f"\n{'='*60}")
    print("📊 BATCH FELDOLGOZÁS BEFEJEZVE")
    print(f"{'='*60}")
    print(f"⏱️  Teljes feldolgozási idő: {processing_time:.1f}s")
    print(f"🎼 Összes audio idő: {total_audio_time:.1f}s")
    print(f"📊 Sebesség: {total_audio_time/processing_time:.1f}x realtime" if processing_time > 0 else "")
    print(f"✅ Sikeres fájlok: {len(results)}")
    print(f"❌ Hibás fájlok: {len(errors)}")
    
    return results, errors, processing_time


def save_results_tensorflow(results, errors):
    """Eredmények mentése fejlett statisztikákkal"""
    saved_files = []
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Sikeres eredmények mentése
    if results:
        df = pd.DataFrame(results)
        results_file = f"speed_eredmenyek_{timestamp}.csv"
        df.to_csv(results_file, index=False, encoding='utf-8-sig')
        print(f"\n💾 Eredmények mentve: {results_file}")
        saved_files.append(results_file)
        
        # Részletes statisztikák
        print(f"\n📈 RÉSZLETES STATISZTIKÁK:")
        print("-" * 40)
        print(f"  • Fájlok száma: {len(df)}")
        print(f"  • Átlagos BPM: {df['BPM'].mean():.1f}")
        print(f"  • BPM tartomány: {df['BPM'].min():.1f} - {df['BPM'].max():.1f}")
        print(f"  • Átlagos feldolgozási idő: {df['feldolgozasi_ido_sec'].mean():.1f}s")
        
        # Legnépszerűbb műfajok
        if 'Genre_1' in df.columns:
            top_genres = df['Genre_1'].value_counts().head(3)
            print(f"  • Legnépszerűbb műfajok:")
            for genre, count in top_genres.items():
                print(f"    - {genre}: {count} fájl")
        
        # Konfidencia statisztikák
        if 'Conf_1' in df.columns:
            print(f"  • Átlagos konfidencia: {df['Conf_1'].mean():.1%}")
            print(f"  • Magas konfidencia (>50%): {(df['Conf_1'] > 0.5).sum()} fájl")
    
    # Hibák mentése
    if errors:
        df_errors = pd.DataFrame(errors)
        errors_file = f"speed_hibak_{timestamp}.csv"
        df_errors.to_csv(errors_file, index=False, encoding='utf-8-sig')
        print(f"\n⚠️ Hibák mentve: {errors_file}")
        saved_files.append(errors_file)
    
    return saved_files


def main():
    """
    Fő függvény - TensorFlow alapú műfaj elemzés
    """
    print("⚡ ESSENTIA SEBESSÉG OPTIMALIZÁLT MŰFAJ ELEMZŐ")
    print("="*60)
    print("🤖 Discogs EffNet - BPM + műfaj optimális sebességgel")
    print("🔧 Javítások: Essentia resample + vectorizált top-k")
    print("="*60)
    
    try:
        # Osztályozó inicializálása
        classifier = MusicGenreClassifier()
        
        # Modell fájlok letöltése
        print("\n1️⃣ Modell fájlok ellenőrzése...")
        if not classifier.download_models():
            print("❌ Modell letöltés sikertelen!")
            return 1
        
        # Modell betöltése
        print("\n2️⃣ TensorFlow modell betöltése...")
        if not classifier.load_model():
            print("❌ Modell betöltés sikertelen!")
            return 1
        
        # Audio fájlok keresése
        print("\n3️⃣ Audio fájlok keresése...")
        audio_files, audio_dir = check_audio_directory()
        
        if not audio_files:
            print(f"\n⚠️ Nincs feldolgozható fájl!")
            print(f"📁 Helyezz audio fájlokat a '{audio_dir}' könyvtárba")
            print("🎵 Támogatott formátumok: MP3, WAV, FLAC, OGG, M4A")
            return 0
        
        # Batch feldolgozás
        print(f"\n4️⃣ TensorFlow batch feldolgozás...")
        results, errors, proc_time = process_batch_tensorflow(
            classifier, audio_files, audio_dir
        )
        
        # Eredmények mentése
        print(f"\n5️⃣ Eredmények mentése...")
        saved_files = save_results_tensorflow(results, errors)
        
        print(f"\n🎉 FELDOLGOZÁS BEFEJEZVE!")
        print(f"💾 Mentett fájlok: {', '.join(saved_files)}")
        print(f"⏱️  Teljes idő: {proc_time:.1f} másodperc")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Feldolgozás megszakítva")
        return 1
    except Exception as e:
        print(f"\n❌ Váratlan hiba: {e}")
        import traceback
        traceback.print_exc()
        return 1


def silent_main():
    """Main wrapper - elnyomja az összes stderr outputot"""
    # Stderr elnyomás a teljes program futása alatt
    stderr_devnull = open(os.devnull, 'w')
    original_stderr = sys.stderr
    
    try:
        # Csak a WARNING és INFO szintű üzenetek elnyomása
        class WarningFilter:
            def write(self, text):
                # Ha WARNING vagy INFO, ne írja ki
                if any(keyword in text for keyword in ['WARNING', 'INFO', 'No network created']):
                    return
                # Egyébként eredeti stderr-re
                original_stderr.write(text)
                
            def flush(self):
                original_stderr.flush()
        
        sys.stderr = WarningFilter()
        return main()
        
    finally:
        sys.stderr = original_stderr
        stderr_devnull.close()


if __name__ == "__main__":
    sys.exit(silent_main())