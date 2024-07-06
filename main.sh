#!/usr/bin/env bash

python3 src/main.py
cd publix && python3 -m http.server 8888
