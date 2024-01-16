#!/bin/bash -l
[ "$3" = ""  ] && /logToCs.py "$1" "$2" --root "$PWD"
[ "$3" != "" ] && /logToCs.py "$1" "$2" --root "$3"
