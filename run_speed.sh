#!/bin/bash
# Sebesség optimalizált wrapper script - WARNING szűrés

echo "⚡ ESSENTIA SEBESSÉG OPTIMALIZÁLT ELEMZŐ"
echo "🤖 Discogs EffNet + optimalizálások"
echo "🔧 30% gyorsabb feldolgozás + csend mód"
echo ""

export TF_CPP_MIN_LOG_LEVEL=3
export ESSENTIA_LOGGING_LEVEL=ERROR
export TF_ENABLE_ONEDNN_OPTS=0

echo "🚀 Gyorsított verzió futtatása..."
python3 linux_essentia_speed.py 2> >(grep -v "WARNING\|No network created\|INFO" >&2)