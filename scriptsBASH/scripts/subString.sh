#!/bin/bash
if echo "$2" | grep -q "$1"; then
    echo "$1 está contida em $2"
else
    echo "$1 não está contida em $2"
fi