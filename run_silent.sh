#!/bin/bash
# Csend wrapper script - Discogs EffNet modell (400+ műfaj)

echo "🎯 ESSENTIA OPTIMALIZÁLT MŰFAJ ELEMZŐ"
echo "🤖 Discogs EffNet modell - 400+ műfaj kategória"
echo "📊 Professzionális minőségű eredmények"
echo ""

export TF_CPP_MIN_LOG_LEVEL=3
export ESSENTIA_LOGGING_LEVEL=ERROR
export TF_ENABLE_ONEDNN_OPTS=0

echo "🚀 Futtatás optimalizált verzióval..."
python3 linux_essentia_optimized.py 2> >(grep -v "WARNING\|No network created" >&2)