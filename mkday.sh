#!/usr/bin/env bash

set -eux

mkdir $1

cp template.py $1/main.py
curl --cookie "session=$(cat .SESSION)" "https://adventofcode.com/2024/day/$1/input" > "$1/inp.txt"
