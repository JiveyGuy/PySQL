#!/bin/bash
rm -rf dist
mkdir dist
python3 -m nuitka src --report=out.xml --onefile --output-dir=dist --enable-plugin=tk-inter --jobs=64 --run --assume-yes-for-downloads --include-package-data=customtkinter --linux-icon=./src/PySQL.jpg --follow-imports