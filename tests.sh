#!/bin/sh
# Tests

echo "#,scheweRabit,scheweNoRabit,spotRabit,spotNoRabit"

i=0
TIMEOUT="1h"
for FILE in benchmark/*; do
    i="${FILE:11}"
    echo -n "${i},"
    
    # schewe with rabit
    timeout "$TIMEOUT" python main.py --rabit <"$FILE" >/dev/null
    status=$?
    if [[ $status -eq 124 ]] ; then
        echo -n "TO,"
        success="false"
    elif [[ $status -eq 137 ]] ; then
        echo -n "OOM,"
        success="false"
    else
        echo -n "${status},"
        success="true"
    fi
    
    # schewe without rabit
    if [[ $success -eq "true" ]] ; then
        timeout "$TIMEOUT" python main.py <"$FILE" >/dev/null
        status=$?
    fi
    if [[ $status -eq 124 ]] ; then
        echo -n "TO,"
    elif [[ $status -eq 137 ]] ; then
        echo -n "OOM,"
    else
        echo -n "${status},"
    fi
    
    # spot with rabit
    timeout "$TIMEOUT" python main.py --spot --rabit <"$FILE" >/dev/null
    status=$?
    if [[ $status -eq 124 ]] ; then
        echo -n "TO,"
        success="false"
    elif [[ $status -eq 137 ]] ; then
        echo -n "OOM,"
        success="false"
    else
        echo -n "${status},"
        success="true"
    fi
    
    # spot without rabit
    timeout "$TIMEOUT" python main.py --spot <"$FILE" >/dev/null
    status=$?
    if [[ $status -eq 124 ]] ; then
        echo "TO,"
    elif [[ $status -eq 137 ]] ; then
        echo -n "OOM,"
    else
        echo "${status},"
    fi
done
