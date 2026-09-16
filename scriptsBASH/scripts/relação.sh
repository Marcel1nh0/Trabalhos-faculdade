#!/bin/bash
if [ $1 -lt $2 ]; then
    echo "$1 é menor que $2"
elif [ $1 -gt $2 ]; then
    echo "$1 é maior que $2"
else
    echo "Os números são iguais"
fi