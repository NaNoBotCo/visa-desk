#!/bin/sh
cd "$(dirname "$0")" || exit 1
open "http://localhost:4173/"
cd site && exec python3 -m http.server 4173
