#!/bin/sh -l
ANNOTATE=""
LOGTOCS=$(realpath "$(dirname "$0")/logToCs.py")
if [[ "$(uname -a)" =~ "MINGW"* ]] || [[ "$(uname -a)" =~ "CYGWIN"* ]] ; then
    LOGTOCS=$(cygpath -w "${LOGTOCS}")
fi

[ "$3" = "true" ] && ANNOTATE="--github-annotate"
[ "$3" = "false" ] && ANNOTATE="--no-github-annotate"
[ "$3" = ""  ] && python ./logToCs.py "$1" "$2" --root "$PWD" && exit 0
[ "$3" != "" ] && python ./logToCs.py "$1" "$2" --root "$3"   && exit 0
