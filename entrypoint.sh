#!/bin/sh -l
ANNOTATE=""
LOGTOCS=$(realpath "$(dirname "$0")/logToCs.py")
case "$(uname -a)" in
    MINGW*|CYGWIN*)
        LOGTOCS=$(cygpath -w "${LOGTOCS}")
        ;;
    *)
        ;;
esac

[ "$4" = "true" ] && ANNOTATE="--github-annotate"
[ "$4" = "false" ] && ANNOTATE="--no-github-annotate"
[ "$3" = ""  ] && python ./logToCs.py "$1" "$2" --root "$PWD" ${ANNOTATE} && exit 0
[ "$3" != "" ] && python ./logToCs.py "$1" "$2" --root "$3"   ${ANNOTATE} && exit 0
