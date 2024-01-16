#!/bin/bash -lxv
[ "$3" = ""  ] && python /logToCs.py "$1" "$2" --root "$PWD"
[ "$3" != "" ] && python /logToCs.py "$1" "$2" --root "$3"
