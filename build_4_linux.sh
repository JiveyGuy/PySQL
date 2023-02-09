#!/bin/bash
rm -rf dist
mkdir dist
python3.10 -m nuitka src --report=out.xml \
    --onefile \
    --output-dir=dist \
    --enable-plugin=tk-inter \
    --jobs=64 \
    --assume-yes-for-downloads \
    --include-package-data=customtkinter \
    --linux-icon=src/logo.png \
    --follow-imports \
    --include-data-file=src/logo.png=logo.png 
    # --run 