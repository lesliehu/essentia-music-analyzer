#!/bin/bash
# Teljesen csend wrapper script

export TF_CPP_MIN_LOG_LEVEL=3
export ESSENTIA_LOGGING_LEVEL=ERROR
export TF_ENABLE_ONEDNN_OPTS=0

# Stderr redirect csak a warning-okhoz
python3 linux_essentia_optimized.py 2> >(grep -v "WARNING\|No network created" >&2)