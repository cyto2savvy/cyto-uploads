#!/usr/bin/env bash
# Cyto v2 canon + animation tests. Exit 0 = all pass.  Usage: bash studio/branding/rebrand-v2/run_tests.sh
set -e
cd "$(dirname "$0")"
python3 -I test_cyto.py
