#!/bin/bash
# Apple Silicon optimalizált wrapper script

echo "🍎 ESSENTIA APPLE SILICON MŰFAJ ELEMZŐ"
echo "🤖 M1/M2/M3 chip optimalizációkkal"
echo "🔧 Metal GPU + Accelerate framework + ARM64"
echo ""

# Apple Silicon specifikus környezeti változók
export TF_CPP_MIN_LOG_LEVEL=3
export ESSENTIA_LOGGING_LEVEL=ERROR
export TF_ENABLE_ONEDNN_OPTS=0

# Apple Accelerate framework optimalizáció
export VECLIB_MAXIMUM_THREADS=$(sysctl -n hw.ncpu)
export OPENBLAS_NUM_THREADS=$(sysctl -n hw.ncpu)
export MKL_NUM_THREADS=$(sysctl -n hw.ncpu)

# TensorFlow Metal GPU
export TF_METAL=1
export TF_ENABLE_MLIR_OPTIMIZATIONS=1

# Platform check
if [[ $(uname -m) == "arm64" ]]; then
    echo "✅ Apple Silicon (ARM64) platform detektálva"
else
    echo "⚠️  Figyelem: Nem Apple Silicon platform ($(uname -m))"
fi

echo "🚀 Apple Silicon optimalizált verzió futtatása..."
python3 apple_essentia_silicon.py 2> >(grep -v "WARNING\|No network created\|INFO" >&2)