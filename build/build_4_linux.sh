#!/bin/bash
rm -rf dist
mkdir dist
python3.10 $(<nuitka_command_linux.txt)