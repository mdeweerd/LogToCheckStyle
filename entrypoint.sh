#!/bin/bash -lxv
[ "$3" = ""  ] && python /logToCs.py "$1" "$2" --root "$PWD" && exit 0
[ "$3" != "" ] && python /logToCs.py "$1" "$2" --root "$3"   && exit 0
