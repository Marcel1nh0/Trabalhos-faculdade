#!/bin/bash
i=1
while [ $# -gt 0 ]; do
    echo "Parâmetro $i: $1"
    i=$((i + 1))
    shift
done