#!/bin/bash


while IFS=: read usuario senha id grupo nome resto
do
    
    echo -e "$usuario\t$nome"
done < /etc/passwd