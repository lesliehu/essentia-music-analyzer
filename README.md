# Essentia Zene Műfaj Elemző - Multi-Platform

**🎯 ÁLLAPOT**: Optimalizált rendszer! Egyetlen profi modell - Discogs EffNet 400+ műfajjal.

**🖥️ PLATFORMOK**: 
- 🐧 **Linux x86_64** - Teljes funkcionalitás
- 🍎 **Apple Silicon (M1/M2/M3)** - 2x gyorsabb, Metal GPU optimalizáció

## 🚀 Gyors Indítás

### 🐧 Linux x86_64:
```bash
# 1. Telepítés
chmod +x setup.sh && ./setup.sh

# 2. Git LFS modellek
git lfs pull

# 3. Audio fájlok hozzáadása
cp *.mp3 audio_mp3/

# 4. Futtatás
./run_silent.sh
```

### 🍎 Apple Silicon (M1/M2/M3):
```bash
# 1. Telepítés
chmod +x setup_apple.sh && ./setup_apple.sh

# 2. Git LFS modellek
git lfs pull

# 3. Audio fájlok hozzáadása
cp *.mp3 audio_mp3/

# 4. Futtatás (2x gyorsabb!)
source essentia_apple_env/bin/activate
./run_apple.sh
```

## 📁 Rendszer Struktúra

```
essentia-local/
├── 🐧 LINUX x86_64:
│   ├── linux_essentia_optimized.py   # FŐPROGRAM - Discogs EffNet
│   ├── linux_essentia_speed.py       # GYORSÍTOTT verzió (30% gyorsabb)
│   ├── run_silent.sh                  # Wrapper (eredeti verzió csend)
│   ├── run_speed.sh                   # Wrapper (gyorsított verzió csend)
│   ├── setup.sh                      # Telepítő script
│   ├── requirements.txt              # Python függőségek
│   └── check_installation.py         # Telepítés ellenőrző
├── 🍎 APPLE SILICON (M1/M2/M3):
│   ├── apple_essentia_silicon.py     # APPLE optimalizált verzió (2x gyorsabb!)
│   ├── run_apple.sh                  # Apple wrapper script
│   ├── setup_apple.sh                # Apple telepítő script
│   └── requirements_apple.txt        # Apple függőségek (Metal GPU)
├── 📂 KÖZÖS:
│   ├── models/                       # Modell fájlok  
│   │   ├── classifier_model.pb       # Discogs EffNet (18MB)
│   │   └── classifier_labels.json    # 400 műfaj címke
│   ├── audio_mp3/                    # Feldolgozandó fájlok
│   └── README.md                     # Ez a fájl
```

## 🎼 Jellemzők

### 🚀 **Egyszerű, Optimalizált Megközelítés:**

#### **Discogs EffNet Elemző** (`linux_essentia_optimized.py`)
- **400+ műfaj kategória**: Professzionális részletezettség
- **Rögzített beállítások**: Plug-and-play használat  
- **Csend üzemmód**: Tiszta, spam-mentes kimenet
- **Optimalizált teljesítmény**: 15-30 másodperc/fájl
- **Kompakt méret**: Csak 18MB modell + kód

### 🔧 **Beépített Funkciók:**
- **Batch feldolgozás**: Több fájl egyszerre 
- **BPM elemzés**: Automatikus tempó meghatározás
- **CSV export**: Strukturált, UTF-8 eredmények
- **TensorFlow optimalizálás**: Nagy teljesítmény
- **Wrapper script**: Egy parancsból futtatható

## 📊 Műfaj Kategóriák (Példák)

```
Blues → Chicago Blues, Delta Blues, Electric Blues...
Electronic → House, Techno, Trance, Ambient...
Rock → Alternative, Heavy Metal, Progressive...
Hip Hop → Boom Bap, Trap, Conscious...
Jazz → Bebop, Fusion, Smooth Jazz...
Pop → Indie Pop, K-pop, Dance-pop...
Classical → Baroque, Contemporary, Opera...
```

## 🎯 **Discogs EffNet Modell Jellemzők**

| Tulajdonság | Érték |
|-------------|-------|
| **Műfajok száma** | 400+ részletes kategória |
| **Pontosság** | ⭐⭐⭐⭐⭐ Professzionális szint |
| **Sebesség** | 15-30 másodperc/fájl |
| **Modell méret** | 18MB (optimalizált) |
| **Használat** | Professzionális elemzés |

### **Miért csak Discogs EffNet:**
- 🎯 **Precíz eredmények**: "Progressive House" vs "Tech House" megkülönböztetés
- 🎼 **Professzionális minőség**: DJ-k, zenei adatbázisok, kutatás
- 📊 **Részletes kategóriák**: 400+ műfaj vs 10 alapkategória
- 🔧 **Egyszerűség**: Egy modell, egy minőségi standard
- 💾 **Optimális**: Minimális tárhely (18MB vs 65MB előtte)

## 💻 Hardware Követelmények

### 🐧 Linux x86_64:
| Komponens | Minimum | Ajánlott |
|-----------|---------|----------|
| **CPU** | 2 core, 2GHz | 4+ core, 3GHz+ |
| **RAM** | 4GB | 8-16GB |
| **Tárhely** | 2GB | 10GB+ |
| **OS** | Linux x86_64 | Ubuntu 22.04+ |

**Teljesítmény**: 8-15 másodperc/fájl (optimalizált verzió)

### 🍎 Apple Silicon (M1/M2/M3):
| Komponens | Specifikáció |
|-----------|--------------|
| **Chip** | Apple M1/M2/M3 (ARM64) |
| **RAM** | 8GB+ (Metal GPU optimalizálva) |
| **Tárhely** | 2GB |
| **OS** | macOS Big Sur+ (11.0+) |

**Teljesítmény**: 4-8 másodperc/fájl (**2x gyorsabb** mint Linux!)
**🚀 Példa**: 199.5s audio → 4.1s feldolgozás = **48.6x realtime**

## 🔧 Telepítés Részletesen

### 🐧 Linux Automatikus:
```bash
./setup.sh
```

### 🍎 Apple Silicon Automatikus:
```bash
./setup_apple.sh
```

### 🐧 Linux Manuális:
```bash
python3 -m venv essentia_env
source essentia_env/bin/activate
pip install essentia-tensorflow numpy pandas
mkdir -p audio_mp3
```

### 🍎 Apple Silicon Manuális:
```bash
python3 -m venv essentia_apple_env
source essentia_apple_env/bin/activate
pip install -r requirements_apple.txt
mkdir -p audio_mp3
```

## 📝 Használat

### **🐧 Linux Használat**

#### **1. Wrapper Scriptek (Ajánlott)**
```bash
# Eredeti verzió csend módban
./run_silent.sh

# Gyorsított verzió csend módban (30% gyorsabb)
./run_speed.sh
```

#### **2. Közvetlen Futtatás**
```bash
# Audio fájlok hozzáadása
cp your_music.mp3 audio_mp3/

# Futtatás
source essentia_env/bin/activate
python3 linux_essentia_optimized.py
```

### **🍎 Apple Silicon Használat (2x Gyorsabb!)**

#### **1. Wrapper Script (Ajánlott)**
```bash
# Apple optimalizált verzió csend módban
source essentia_apple_env/bin/activate
./run_apple.sh
```

#### **2. Közvetlen Futtatás**
```bash
# Audio fájlok hozzáadása
cp your_music.mp3 audio_mp3/

# Apple Silicon verzió futtatása
source essentia_apple_env/bin/activate  
python3 apple_essentia_silicon.py
```

### **📂 Eredmények:**
- **Linux**: `tensorflow_eredmenyek_*.csv` / `speed_eredmenyek_*.csv`
- **Apple Silicon**: `apple_silicon_eredmenyek_*.csv`
- **Hibák**: `*_hibak_*.csv`

### **CSV Formátum:**
```csv
fajl,BPM,modell,Genre_1,Conf_1,Genre_2,Conf_2,...
song.mp3,128.5,discogs,"Electronic / House",0.8432,"Pop / Dance-pop",0.1234
rock.mp3,161.5,discogs,"Rock / Alternative",0.7234,"Rock / Heavy Metal",0.1876
```

## 📈 Támogatott Formátumok

- **Audio**: MP3, WAV, FLAC, OGG, M4A
- **Kimenet**: CSV (UTF-8 with BOM)

## ⚡ Optimalizálás

### CPU teljesítmény:
```bash
# Performance mód
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# CPU affinity
taskset -c 0-3 python3 linux_essentia_optimized.py
```

### Környezeti változók:
```bash
export TF_CPP_MIN_LOG_LEVEL=2
export OMP_NUM_THREADS=4
python3 linux_essentia_optimized.py
```

## 🐛 Hibaelhárítás

### Telepítési problémák ellenőrzése:
```bash
source essentia_env/bin/activate
python3 check_installation.py
```

### "Essentia nincs telepítve":
```bash
pip install essentia-tensorflow==2.1b6.dev1389
```

### Git LFS modell problémák:
```bash
sudo apt install git-lfs
git lfs install
git lfs pull
ls -lah models/classifier_model.pb  # ~18MB kell legyen
```

### "TensorFlow WARNING" üzenetek:
A program automatikusan elcsendesíti őket, de ha mégis megjelennek:
```bash
export TF_CPP_MIN_LOG_LEVEL=3
python3 linux_essentia_optimized.py
```

### Lassú feldolgozás:
- Több CPU core használata  
- SSD használata HDD helyett
- Kisebb fájlokkal tesztelés

### Memória problémák:
```bash
# Swap hozzáadása
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## ☁️ Cloud Futtatás

### AWS EC2:
- Instance: c5.xlarge (4 vCPU, 8GB)
- Ubuntu 22.04 AMI

### Google Cloud:
- Instance: n2-standard-4 (4 vCPU, 16GB)
- Ubuntu 22.04 LTS

## 🔄 Batch Feldolgozás

Nagy mennyiségű fájlhoz:
```bash
# Több fájl egy könyvtárból
cp /path/to/music/*.mp3 audio_mp3/

# Futtatás háttérben
nohup python3 linux_essentia_optimized.py > output.log 2>&1 &

# Progress követése
tail -f output.log
```

## 📞 Támogatás

- **Rendszer teszt**: A gyors tesztelő script törölve lett - használd közvetlenül a főprogramot
- **Logok**: stderr és stdout a terminálban
- **Debug**: `TF_CPP_MIN_LOG_LEVEL=0` részletes TensorFlow logokhoz

---

## 🎯 **Összefoglalás**

**Multi-platform optimalizált rendszer:**
- ✅ **18MB** kompakt rendszer (47MB-ról csökkentve)
- ✅ **400+ műfaj** professzionális pontossággal  
- ✅ **Multi-platform**: Linux x86_64 + Apple Silicon
- ✅ **Apple Silicon 2x gyorsabb**: 4-8s/fájl vs 8-15s/fájl
- ✅ **Metal GPU optimalizáció**: TensorFlow Apple Silicon
- ✅ **Egyszerű használat** - egy parancs, megbízható eredmény
- ✅ **Tiszta architektúra** - nincs felesleges komplexitás

**🍎 Apple Silicon kiemelkedő teljesítmény**: 199.5s audio → 4.1s feldolgozás = **48.6x realtime!**

**A rendszer készen áll mindkét platformon! Optimális tárhely, maximális pontosság, professzionális eredmények.**