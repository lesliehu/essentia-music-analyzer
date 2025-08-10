#!/bin/bash
# Intelligens csend wrapper script - automatikus verzió választás

export TF_CPP_MIN_LOG_LEVEL=3
export ESSENTIA_LOGGING_LEVEL=ERROR
export TF_ENABLE_ONEDNN_OPTS=0

# Konfiguráció ellenőrzése
if [ -f "config.json" ]; then
    echo "🔧 Config.json található - konfigurálható verzió használata"
    echo "📋 Aktív konfiguráció:"
    python3 config_editor.py show | head -10
    echo ""
    echo "🚀 Futtatás konfigurálható verzióval..."
    python3 linux_essentia_configurable.py 2> >(grep -v "WARNING\|No network created" >&2)
else
    echo "📁 Config.json hiányzik - optimalizált verzió használata"
    echo "🚀 Futtatás optimalizált verzióval..."
    python3 linux_essentia_optimized.py 2> >(grep -v "WARNING\|No network created" >&2)
fi