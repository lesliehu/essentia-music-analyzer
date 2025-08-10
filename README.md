# Essentia Zene Műfaj Elemző - Linux x86

**🎯 ÁLLAPOT**: Rendszer kész a használatra! TensorFlow Discogs EffNet modell 400+ műfajjal.

## 🚀 Gyors Indítás

```bash
# 1. Telepítés
chmod +x setup.sh && ./setup.sh

# 2. Telepítés ellenőrzés
source essentia_env/bin/activate
python3 check_installation.py

# 3. Git LFS modellek (ha szükséges)
git lfs pull

# 4. Audio fájlok hozzáadása
cp *.mp3 audio_mp3/

# 5. Futtatás (csend verzió)
python3 linux_essentia_optimized.py
```

## 📁 Rendszer Struktúra

```
essentia-local/
├── linux_essentia_optimized.py    # FŐPROGRAM (csend verzió)
├── linux_essentia_configurable.py # KONFIGURÁLHATÓ verzió
├── config.json                    # Konfiguráció fájl
├── config_editor.py               # Konfiguráció szerkesztő
├── check_installation.py          # Telepítés ellenőrző
├── setup.sh                       # Telepítő script  
├── requirements.txt               # Python függőségek
├── README.md                      # Ez a fájl
├── models/                        # Aktív modellek
│   ├── classifier_model.pb        # Discogs EffNet (18MB)
│   └── classifier_labels.json     # 400 műfaj címke
├── essentia-models/               # További modellek
│   ├── effnetdiscogs/             # Discogs EffNet
│   ├── musicnn/                   # MusiCNN (10 műfaj)
│   ├── vgg/                       # VGG4
│   └── ...                        # További opciók
└── audio_mp3/                     # Feldolgozandó fájlok
```

## 🎼 Jellemzők

### 🚀 **Két Verzió Elérhető:**

#### **1. Optimalizált Verzió** (`linux_essentia_optimized.py`)
- **Discogs EffNet modell**: 400+ műfaj kategória
- **Rögzített beállítások**: Gyors használat
- **Csend üzemmód**: Nincs TensorFlow spam

#### **2. Konfigurálható Verzió** (`linux_essentia_configurable.py`) 
- **Több modell támogatás**: Discogs EffNet ÉS MusiCNN
- **JSON konfiguráció**: Testreszabható beállítások
- **Interaktív szerkesztő**: `config_editor.py`
- **Teljesítmény választás**: Gyors vs pontos

### 🔧 **Közös Jellemzők:**
- **Batch feldolgozás**: Több fájl egyszerre 
- **BPM elemzés**: Automatikus tempó meghatározás
- **CSV export**: Strukturált eredmények
- **TensorFlow optimalizálás**: Nagy teljesítmény

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

## 🎭 **Modell Összehasonlítás**

| Modell | Műfajok | Sebesség | Pontosság | Használat |
|--------|---------|----------|-----------|-----------|
| **Discogs EffNet** | 400+ | Lassú | ⭐⭐⭐⭐⭐ | Professzionális elemzés |
| **MusiCNN** | 10 | Gyors | ⭐⭐⭐⭐ | Gyors kategorizálás |

### **Mikor használj melyiket:**

#### **Discogs EffNet** - Ha kell a precizitás:
- 🎯 **Részletes műfajok**: "Progressive House" vs "Tech House"  
- 🎼 **Professzionális használat**: DJ-k, zenei adatbázisok
- 📊 **Kutatás, statisztikák**: Pontos kategorizálás
- ⏳ **Van idő**: 15-30 másodperc/fájl

#### **MusiCNN** - Ha kell a sebesség:
- ⚡ **Gyors screening**: Alapvető műfaj meghatározás
- 📁 **Nagy mennyiség**: 1000+ fájl batch feldolgozás
- 🔄 **Valós idejű**: Streaming alkalmazások
- ⏱️ **Gyors eredmény**: 3-8 másodperc/fájl

## 💻 Hardware Követelmények

| Komponens | Minimum | Ajánlott |
|-----------|---------|----------|
| **CPU** | 2 core, 2GHz | 4+ core, 3GHz+ |
| **RAM** | 4GB | 8-16GB |
| **Tárhely** | 5GB | 20GB+ |
| **OS** | Linux x86_64 | Ubuntu 22.04+ |

**Teljesítmény**: 15-60 másodperc/fájl (géptől függően)

## 🔧 Telepítés Részletesen

### Automatikus:
```bash
./setup.sh
```

### Manuális:
```bash
python3 -m venv essentia_env
source essentia_env/bin/activate
pip install essentia-tensorflow numpy pandas
mkdir -p audio_mp3
```

## 📝 Használat

### **1. Egyszerű Használat** (Optimalizált Verzió)
```bash
# Audio fájlok hozzáadása
cp your_music.mp3 audio_mp3/

# Futtatás (Discogs EffNet modell)
source essentia_env/bin/activate
python3 linux_essentia_optimized.py
```

### **2. Konfigurálható Használat** (Több Modell)
```bash
# Konfiguráció megtekintése
python3 config_editor.py show

# Modell váltás (MusiCNN gyorsabb)
python3 config_editor.py set-model musicnn

# Konfigurálható futtatás
python3 linux_essentia_configurable.py
```

### **3. Interaktív Konfiguráció**
```bash
# Grafikus szerkesztő
python3 config_editor.py
# ↓ Menü:
# 1. Konfiguráció megjelenítése
# 2. Elérhető modellek
# 3. Aktív modell változtatása  
# 4. Feldolgozási beállítások
```

### **Eredmények:**
- **Optimalizált**: `tensorflow_eredmenyek_*.csv`
- **Konfigurálható**: `music_analysis_[model]_*.csv`
- **Hibák**: `*_hibak_*.csv` (ha vannak)

### **CSV Formátum:**
```csv
fajl,BPM,modell,Genre_1,Conf_1,Genre_2,Conf_2,...
song.mp3,128.5,discogs,"Electronic / House",0.8432,"Pop / Dance-pop",0.1234
song2.mp3,95.2,musicnn,"rock",0.7234,"electronic",0.1876
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

**A rendszer készen áll a használatra! Egyszerű telepítés, pontos eredmények, professzionális CSV kimenetek.**