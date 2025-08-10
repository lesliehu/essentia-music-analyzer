# Essentia Zene Műfaj Elemző - Linux x86

**🎯 ÁLLAPOT**: Rendszer kész a használatra! TensorFlow Discogs EffNet modell 400+ műfajjal.

## 🚀 Gyors Indítás

```bash
# 1. Telepítés
chmod +x setup.sh && ./setup.sh

# 2. Audio fájlok hozzáadása
cp *.mp3 audio_mp3/

# 3. Futtatás
source essentia_env/bin/activate
python3 linux_essentia_optimized.py
```

## 📁 Rendszer Struktúra

```
essentia-local/
├── linux_essentia_optimized.py    # FŐPROGRAM
├── setup.sh                       # Telepítő script
├── requirements.txt               # Python függőségek
├── README.md                      # Ez a fájl
├── models/                        # Aktív modellek
│   ├── classifier_model.pb        # Discogs EffNet (17MB)
│   └── classifier_labels.json     # 400 műfaj címke
├── essentia-models/               # További modellek
│   ├── effnetdiscogs/             # Discogs EffNet
│   ├── musicnn/                   # MusiCNN (10 műfaj)
│   ├── vgg/                       # VGG4
│   └── ...                        # További opciók
└── audio_mp3/                     # Feldolgozandó fájlok
```

## 🎼 Jellemzők

- **Discogs EffNet modell**: 400+ műfaj kategória
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

### Egyszerű használat:
```bash
# Fájlok hozzáadása
cp your_music.mp3 audio_mp3/

# Elemzés futtatása
source essentia_env/bin/activate
python3 linux_essentia_optimized.py
```

### Eredmények:
- `tensorflow_eredmenyek_YYYYMMDD_HHMMSS.csv` - Sikeres elemzések
- `tensorflow_hibak_YYYYMMDD_HHMMSS.csv` - Hibás fájlok (ha vannak)

### CSV formátum:
```csv
fajl,BPM,audio_hossz_sec,Genre_1,Conf_1,Genre_2,Conf_2,...
song.mp3,128.5,180.2,"Electronic / House",0.8432,"Pop / Dance-pop",0.1234
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

### "Essentia nincs telepítve":
```bash
pip install essentia-tensorflow
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